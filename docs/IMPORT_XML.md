# How to Import Custom XML Cleaners into BleachBit

BleachBit allows you to extend its cleaning capabilities by importing custom cleaner definition files (XML files). This guide explains how to do it.

## Method 1: Using the BleachBit Interface (Recommended)

This is the easiest and safest method for most users.

1.  **Open BleachBit.**
2.  **Go to Preferences:**
    *   On Windows/Linux: Click on the **Edit** menu (it might be a "hamburger" icon ☰ or similar depending on your version/theme) and select **Preferences**.
    *   On macOS: Click on **BleachBit** in the menu bar and select **Preferences**.
3.  **Navigate to the "Cleaners" Tab:** In the Preferences window, select the **Cleaners** tab (it might also be labeled "Custom" or similar in older versions).
    ![BleachBit Preferences Cleaners Tab](placeholder_image_preferences_cleaners_tab.png) <!-- Placeholder for an image -->
4.  **Import Cleaner Definitions:**
    *   Look for an option like **"Import"**, **"Add cleaner definitions"**, or a **"+"** button.
    *   Click this button. A file dialog will open.
    *   Navigate to the location where you saved the custom XML cleaner file(s) you downloaded from this project (or created yourself).
    *   Select the XML file(s) and click **Open** or **Import**.
5.  **Confirm and Restart (if prompted):**
    *   BleachBit might ask you to confirm. It may also indicate that a restart of BleachBit is required for the new cleaners to appear.
    *   Close and reopen BleachBit if necessary.
6.  **Find Your New Cleaners:** The newly imported cleaners should now appear in the list of cleaning options in the main BleachBit window, usually under the application name specified in the XML file's `<label>` tag.

## Method 2: Manually Placing XML Files

This method involves copying the XML files directly into BleachBit's custom cleaner folder. This is for more advanced users or if the import function isn't working as expected.

**Caution:** Be careful when manually adding files to application directories. Make sure you are placing them in the correct user-specific folder, not the main program installation folder, to avoid issues with updates or permissions.

1.  **Locate the BleachBit User Cleaner Folder:**
    The location of this folder varies by operating system:
    *   **Windows:** `%AppData%\BleachBit\cleaners`
        *   You can paste this path directly into the File Explorer address bar and press Enter. It typically resolves to `C:\Users\YOUR_USERNAME\AppData\Roaming\BleachBit\cleaners`.
    *   **Linux:** `~/.config/bleachbit/cleaners` or `~/.bleachbit/cleaners` (older versions)
        *   `~` represents your home directory.
    *   **macOS:** `~/Library/Application Support/BleachBit/cleaners`
        *   You might need to unhide your Library folder. In Finder, click Go in the menu bar, hold down the Option key, and Library will appear.

2.  **Create the Folder if it Doesn't Exist:** If the `cleaners` subfolder doesn't exist within the BleachBit user directory, create it.

3.  **Copy the XML Files:** Copy the `.xml` cleaner files you want to add into this `cleaners` folder.

4.  **Restart BleachBit:** Close and reopen BleachBit. The new cleaners should now be loaded and visible in the UI.

## Verifying Imported Cleaners

*   After importing, check the list of cleaners in BleachBit to ensure your new options are present.
*   Always use the **Preview** function in BleachBit before running a new custom cleaner for the first time. This will show you what files the cleaner intends to delete, allowing you to verify its behavior and prevent accidental data loss.

## Troubleshooting

*   **Cleaner Not Appearing:**
    *   Ensure BleachBit was restarted after importing/copying the file.
    *   Double-check that the XML file is valid and well-formed. Errors in the XML can prevent it from loading.
    *   Verify the XML file was placed in the correct directory (for manual method).
*   **Permissions Issues (Manual Method):** Ensure you have the necessary permissions to create folders and copy files into the user-specific BleachBit directory.

By following these steps, you can both manually free up disk space and integrate the cleanup into your regular system maintenance using BleachBit’s flexible custom cleaners.