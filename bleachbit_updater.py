# bleachbit_updater.py

import requests
import re
import argparse
from datetime import datetime
from bs4 import BeautifulSoup
import os
import subprocess
import sys
import logging
from tqdm import tqdm
from typing import Optional, Tuple, Dict

BLEACHBIT_DOWNLOAD_URL = "https://www.bleachbit.org/download"
BLEACHBIT_NEWS_URL = "https://www.bleachbit.org/news"
BLEACHBIT_CI_URL = "https://ci.bleachbit.org/"

# Global debug mode flag
DEBUG_MODE = False

# Initialize logging first
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Configure logging handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler
file_handler = logging.FileHandler('bleachbit_updater.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_latest_bleachbit_versions():
    """Fetches the latest stable and beta BleachBit versions from the website."""
    versions = {"stable": None, "beta": None, "stable_url": None, "beta_url": None}
    try:
        # Try the news page first as it often has direct links and version numbers for recent releases
        response = requests.get(BLEACHBIT_NEWS_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Look for release announcements in the news section
        # This is a heuristic and might need adjustment if the website structure changes
        release_posts = soup.find_all("h2", class_="title") # Common way blog titles are marked

        for post in release_posts:
            title_text = post.get_text().lower()
            link_tag = post.find("a")
            if not link_tag or not link_tag.has_attr("href"):
                continue
            
            post_url = link_tag["href"]
            if not post_url.startswith("http"):
                post_url = "https://www.bleachbit.org" + post_url

            # Check for stable versions (e.g., "BleachBit X.Y.Z")
            stable_match = re.search(r"bleachbit (\d+\.\d+\.\d+)(?!.*beta)(?!.*alpha)", title_text, re.IGNORECASE)
            if stable_match and not versions["stable"]:
                versions["stable"] = stable_match.group(1)
                # Attempt to find a download link on the post page or assume a pattern
                # For simplicity, we'll try to find a .exe link on the download page later
                # or construct it if a pattern is clear.
                # print(f"Found potential stable release post: {title_text}")

            # Check for beta versions (e.g., "BleachBit X.Y.Z beta")
            beta_match = re.search(r"bleachbit (\d+\.\d+\.\d+ beta\s*\d*)", title_text, re.IGNORECASE)
            if beta_match and not versions["beta"]:
                versions["beta"] = beta_match.group(1).replace(" beta", "-beta") # Normalize beta version string
                # print(f"Found potential beta release post: {title_text}")

            if versions["stable"] and versions["beta"]:
                break
        
        # Fallback or supplement with the main download page
        response_dl = requests.get(BLEACHBIT_DOWNLOAD_URL, timeout=10)
        response_dl.raise_for_status()
        soup_dl = BeautifulSoup(response_dl.content, "html.parser")

        # Find download links for Windows
        # Example: <a href="https://download.bleachbit.org/BleachBit-4.6.0-setup.exe">BleachBit 4.6.0 installer</a>
        # Example: <a href="https://download.bleachbit.org/BleachBit-4.9.2-beta-setup.exe">BleachBit 4.9.2 beta installer</a>
        download_links = soup_dl.find_all("a", href=re.compile(r"BleachBit-.*setup\.exe"))

        for link in download_links:
            href = link["href"]
            link_text = link.get_text()

            # Stable version link
            stable_ver_match = re.search(r"BleachBit-(\d+\.\d+\.\d+)-setup\.exe", href)
            if stable_ver_match and not versions["stable_url"]:
                current_ver = stable_ver_match.group(1)
                if not versions["stable"] or versions["stable"] == current_ver:
                    versions["stable"] = current_ver
                    versions["stable_url"] = href
            
            # Beta version link
            beta_ver_match = re.search(r"BleachBit-(\d+\.\d+\.\d+(?:-beta\d*|-beta))-setup\.exe", href)
            if beta_ver_match and not versions["beta_url"]:
                current_ver = beta_ver_match.group(1).replace("-beta", "-beta") # Normalize
                if not versions["beta"] or versions["beta"] == current_ver:
                    versions["beta"] = current_ver
                    versions["beta_url"] = href

        # If version numbers were found from news but URLs not, try to construct them
        # This is a fallback and assumes a consistent naming pattern on download.bleachbit.org
        if versions["stable"] and not versions["stable_url"]:
            versions["stable_url"] = f"https://download.bleachbit.org/BleachBit-{versions['stable']}-setup.exe"
        if versions["beta"] and not versions["beta_url"]:
            # Beta versions might have a number like beta1, beta2, or just beta
            # The regex in news might capture "X.Y.Z beta" or "X.Y.Z beta1"
            # We need to ensure the URL matches the expected format, e.g., X.Y.Z-beta-setup.exe or X.Y.Z-beta1-setup.exe
            beta_version_part = versions["beta"].replace(" ", "-") # Replace space with hyphen if present
            versions["beta_url"] = f"https://download.bleachbit.org/BleachBit-{beta_version_part}-setup.exe"

    except requests.exceptions.RequestException as e:
        print(f"Error fetching BleachBit versions: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching versions: {e}")
    
    return versions

def get_latest_ci_build_url():
    """Fetches the URL for the latest unstable BleachBit build from the CI server."""
    if DEBUG_MODE:
        print(f"[DEBUG] Fetching CI build list from {BLEACHBIT_CI_URL}")
    try:
        response = requests.get(BLEACHBIT_CI_URL, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        latest_build_dir = None
        latest_build_date = None

        # Links to build directories are typically in '<a>' tags
        # Their hrefs look like 'YYYY-MM-DD-HH-MM-SS/'
        for link in soup.find_all("a", href=True):
            href = link['href']
            # Match directory names that look like dates/timestamps
            match = re.match(r"^(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})/$", href)
            if match:
                dir_name = match.group(1)
                if DEBUG_MODE:
                    print(f"[DEBUG] Found potential CI build directory: {dir_name}")
                try:
                    # Attempt to parse the directory name as a datetime object
                    # Example format: 2023-10-27-08-55-00
                    current_date = datetime.strptime(dir_name, "%Y-%m-%d-%H-%M-%S")
                    if latest_build_date is None or current_date > latest_build_date:
                        latest_build_date = current_date
                        latest_build_dir = href
                except ValueError:
                    if DEBUG_MODE:
                        print(f"[DEBUG] Could not parse date from directory: {dir_name}")
                    continue
        
        if not latest_build_dir:
            print("Could not find the latest CI build directory.")
            return None, None

        latest_build_dir_url = BLEACHBIT_CI_URL + latest_build_dir
        if DEBUG_MODE:
            print(f"[DEBUG] Latest CI build directory URL: {latest_build_dir_url}")

        # Now fetch the contents of the latest build directory
        response_build = requests.get(latest_build_dir_url, timeout=15)
        response_build.raise_for_status()
        soup_build = BeautifulSoup(response_build.content, "html.parser")

        # Look for the .exe installer link, typically 'BleachBit-setup.exe'
        for link in soup_build.find_all("a", href=True):
            if link['href'].endswith("BleachBit-setup.exe"):
                installer_url = latest_build_dir_url + link['href']
                # Extract a version/identifier for the CI build, could be the dir name
                ci_version_name = latest_build_dir.strip('/') 
                if DEBUG_MODE:
                    print(f"[DEBUG] Found CI installer: {installer_url} (Version ID: {ci_version_name})")
                return ci_version_name, installer_url
        
        print(f"Could not find BleachBit-setup.exe in {latest_build_dir_url}")
        return None, None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching CI build information: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching CI build: {e}")
    return None, None


def download_bleachbit(url: str, download_path: str = "downloads") -> Optional[str]:
    """Downloads a file from the given URL with progress bar and enhanced error handling."""
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    filename = url.split("/")[-1]
    filepath = os.path.join(download_path, filename)
    
    try:
        logger.info(f"Starting download of {filename} from {url}")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Get file size for progress bar
        total_size = int(response.headers.get('content-length', 0))
        
        # Initialize progress bar
        with open(filepath, 'wb') as f, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                size = f.write(chunk)
                pbar.update(size)
        
        logger.info(f"Successfully downloaded {filename} to {filepath}")
        return filepath
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while downloading BleachBit: {e}")
        if DEBUG_MODE:
            logger.debug(f"Full error details: {e.__class__.__name__}: {str(e)}")
    except IOError as e:
        logger.error(f"File system error while saving download: {e}")
        if DEBUG_MODE:
            logger.debug(f"Full error details: {e.__class__.__name__}: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during download: {e}")
        if DEBUG_MODE:
            logger.exception("Detailed error traceback:")
    return None

def select_version(versions: Dict[str, str], ci_version: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """Interactive version selection with enhanced UI."""
    print("\nAvailable BleachBit versions:")
    print("-" * 40)
    
    options = []
    if versions.get("stable"):
        options.append(("1", f"Stable (v{versions['stable']})", versions.get("stable_url")))
    if versions.get("beta"):
        options.append(("2", f"Beta (v{versions['beta']})", versions.get("beta_url")))
    if ci_version:
        options.append(("3", f"Unstable (CI build: {ci_version})", ci_version))
    
    for num, desc, _ in options:
        print(f"{num}. {desc}")
    print("-" * 40)
    
    while True:
        choice = input("Select version to download (or 'q' to quit): ").strip().lower()
        if choice == 'q':
            return None, None
        
        for num, desc, url in options:
            if choice == num:
                logger.info(f"Selected: {desc}")
                return desc, url
        
        print("Invalid selection. Please try again.")

def run_installer(filepath: str) -> bool:
    """Runs the BleachBit installer."""
    if not filepath or not os.path.exists(filepath):
        logger.error("Installer file not found.")
        return False
    
    try:
        logger.info("Starting BleachBit installer...")
        if os.name == 'nt':
            result = subprocess.run([filepath], check=True)
        else:
            result = subprocess.run(['wine', filepath], check=True)
        
        logger.info("Installation completed successfully.")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Installation failed with return code {e.returncode}")
        if DEBUG_MODE:
            logger.debug(f"Full error details: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during installation: {e}")
        if DEBUG_MODE:
            logger.exception("Detailed error traceback:")
        return False

def main():
    """Main function with enhanced version selection and error handling."""
    parser = argparse.ArgumentParser(description='BleachBit Updater - Fetches and installs BleachBit.')
    parser.add_argument('--version', choices=['stable', 'beta', 'unstable'], help='Specify version to download (stable, beta, unstable). Default is to prompt.')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    global DEBUG_MODE # Declare intent to modify global DEBUG_MODE
    if args.debug:
        DEBUG_MODE = True
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    logger.info("Fetching available BleachBit versions...")
    try:
        logger.info("Fetching available BleachBit versions...")
        versions = get_latest_bleachbit_versions()
        
        logger.debug(f"Found versions: {versions}")
        
        # Get CI build information
        ci_version, ci_url = None, None
        logger.debug("Checking CI server for unstable builds...")
        ci_version, ci_url = get_latest_ci_build_url()

        if not any([versions.get('stable_url'), versions.get('beta_url'), ci_url]):
            logger.error("No BleachBit versions found for download.")
            return

        # Interactive version selection
        selected_desc, download_url = select_version(versions, ci_version)
        if not download_url:
            logger.info("Update cancelled by user.")
            return

        # Download the selected version
        installer_path = download_bleachbit(download_url)
        if not installer_path:
            logger.error("Download failed.")
            return

        # Run the installer
        if run_installer(installer_path):
            logger.info("BleachBit update completed successfully.")
        else:
            logger.error("BleachBit installation failed.")

    except KeyboardInterrupt:
        logger.info("\nUpdate cancelled by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        if logger.isEnabledFor(logging.DEBUG):
            logger.exception("Detailed error traceback:")

def run_installer(filepath):
    """Run the BleachBit installer with appropriate parameters."""
    try:
        logger.info(f"Running installer: {filepath}")
        # For Windows, .exe installers can often be run directly.
        # Adding /S for silent install if supported, common for NSIS installers.
        # This may require admin privileges.
        subprocess.run([filepath, "/S"], check=True)
        logger.info("BleachBit installation/update process started.")
        logger.info("Please follow the on-screen instructions if the installer is not silent.")
        logger.info("You may need to grant administrator privileges.")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running installer: {e}. Try running manually with admin rights.")
    except FileNotFoundError:
        logger.error(f"Error: Installer {filepath} not found or command not executable.")
    except Exception as e:
        logger.error(f"An unexpected error occurred while running the installer: {e}")
    return False

def get_installed_bleachbit_version():
    """Attempts to get the installed BleachBit version on Windows."""
    # Common installation paths for BleachBit
    possible_paths = [
        os.path.join(os.environ.get("ProgramFiles(x86)", ""), "BleachBit", "bleachbit_console.exe"),
        os.path.join(os.environ.get("ProgramFiles", ""), "BleachBit", "bleachbit_console.exe"),
        os.path.join(os.environ.get("LocalAppData", ""), "Programs", "BleachBit", "bleachbit_console.exe") # User install
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                # BleachBit console might output version with --version
                result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5)
                # Expected output: BleachBit X.Y.Z
                match = re.search(r"BleachBit (\d+\.\d+\.\d+)", result.stdout)
                if match:
                    return match.group(1)
            except Exception:
                pass # Ignore errors if version check fails for a path
    return None

def main():
    parser = argparse.ArgumentParser(description="BleachBit Updater Script")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode for verbose output.")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled.")

    logger.info("Checking for BleachBit updates...")
    installed_version = get_installed_bleachbit_version()
    if installed_version:
        logger.info(f"Currently installed BleachBit version: {installed_version}")
    else:
        logger.warning("Could not determine installed BleachBit version. Proceeding to check for latest.")

    latest_versions = get_latest_bleachbit_versions()
    ci_version, ci_url = get_latest_ci_build_url()
    if ci_version and ci_url:
        latest_versions["unstable"] = ci_version
        latest_versions["unstable_url"] = ci_url

    if not latest_versions or (not latest_versions.get("stable_url") and not latest_versions.get("beta_url")):
        logger.error("Could not retrieve latest BleachBit version information.")
        return

    # Show available versions and let user choose
    print("\nAvailable BleachBit versions:")
    if latest_versions.get("stable"):
        print(f"1. Stable: {latest_versions['stable']}")
    if latest_versions.get("beta"):
        print(f"2. Beta: {latest_versions['beta']}")
    if latest_versions.get("unstable"):
        print(f"3. Unstable (CI build): {latest_versions['unstable']}")
    print("n. Cancel update")

    choice = input("\nChoose version to install (1/2/3/n): ").lower().strip()

    url_to_download = None
    chosen_version_type = None

    if choice == '1' and latest_versions.get("stable_url"):
        url_to_download = latest_versions["stable_url"]
        chosen_version_type = "stable"
    elif choice == '2' and latest_versions.get("beta_url"):
        url_to_download = latest_versions["beta_url"]
        chosen_version_type = "beta"
    elif choice == '3' and latest_versions.get("unstable_url"):
        url_to_download = latest_versions["unstable_url"]
        chosen_version_type = "unstable"
    elif choice == 'n':
        logger.info("Update cancelled by user.")
        return
    else:
        logger.error("Invalid choice or version not available.")
        return

    # Download and install the chosen version
    installer_path = download_bleachbit(url_to_download)
    if installer_path:
        if run_installer(installer_path):
            logger.info("BleachBit update completed successfully.")
        else:
            logger.error("Failed to run the installer.")
    else:
        logger.error("Failed to download the installer.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\nUpdate cancelled by user.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        if logger.isEnabledFor(logging.DEBUG):
            logger.exception("Detailed error traceback:")