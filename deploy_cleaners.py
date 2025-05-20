#!/usr/bin/env python3

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

def get_bleachbit_user_dir():
    """Get the user-specific BleachBit cleaners directory based on the OS."""
    if sys.platform == 'win32':
        # Windows: %AppData%\BleachBit\cleaners
        return Path(os.environ['APPDATA']) / 'BleachBit' / 'cleaners'
    elif sys.platform == 'darwin':
        # macOS: ~/Library/Application Support/BleachBit/cleaners
        return Path.home() / 'Library' / 'Application Support' / 'BleachBit' / 'cleaners'
    else:
        # Linux and other Unix-like: ~/.config/bleachbit/cleaners or ~/.bleachbit/cleaners
        config_dir = Path.home() / '.config' / 'bleachbit' / 'cleaners'
        legacy_dir = Path.home() / '.bleachbit' / 'cleaners'
        return config_dir if config_dir.exists() else legacy_dir

def deploy_cleaners():
    """Deploy XML cleaner files to the appropriate BleachBit directory."""
    # Get script directory and source cleaners directory
    script_dir = Path(__file__).resolve().parent
    source_dir = script_dir / 'cleaners'

    # Check if source directory exists
    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}")
        print("Please ensure this script is in the root of the Bleachbit_Clean_Sweep project")
        print("and the 'cleaners' directory exists.")
        return 1

    # Get XML files
    xml_files = list(source_dir.glob('*.xml'))
    if not xml_files:
        print(f"Warning: No .xml files found in {source_dir}")
        print("Nothing to deploy.")
        return 0

    # Get target directory
    target_dir = get_bleachbit_user_dir()
    print(f"Source cleaners directory: {source_dir}")
    print(f"Target BleachBit cleaners directory: {target_dir}")

    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"Ensuring target directory exists: {target_dir}")

    # Function to update paths in XML files after placement
    def update_xml_paths(xml_file_path):
        with open(xml_file_path, 'r') as file:
            content = file.read()
        # Example: Replace placeholder paths with actual paths
        content = content.replace('PLACEHOLDER_PATH', str(get_bleachbit_user_dir()))
        with open(xml_file_path, 'w') as file:
            file.write(content)

    # Copy XML files
    print("\nCopying XML cleaner files...")
    copied_count = 0
    skipped_count = 0

    for xml_file in xml_files:
        try:
            shutil.copy2(xml_file, target_dir)
            print(f"  Copied: {xml_file.name} to {target_dir}")
            copied_count += 1
            # Update paths in the XML file
            update_xml_paths(target_dir / xml_file.name)
        except Exception as e:
            print(f"Error copying {xml_file.name}: {str(e)}")
            skipped_count += 1

    # Print summary
    print("\n" + "-" * 50)
    if copied_count > 0:
        print(f"Successfully copied {copied_count} XML cleaner file(s).")
    if skipped_count > 0:
        print(f"Warning: Skipped {skipped_count} XML cleaner file(s) due to errors.")
    if copied_count == 0 and skipped_count == 0:
        print("No files were processed (this might be unexpected).")

    print("\nDeployment complete.")
    print("Please restart BleachBit if it was running to see the changes.")
    return 0

if __name__ == '__main__':
    try:
        sys.exit(deploy_cleaners())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)