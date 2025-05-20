# How BleachBit Custom Cleaners Work

This document provides an overview of how BleachBit uses XML files to define custom cleaning operations and the basic structure of these XML files.

## BleachBit's Cleaning Mechanism

BleachBit is designed to be extensible. It uses XML files, often called "cleaner definitions" or "CleanerML" (Cleaner Markup Language), to specify what files and registry entries (on Windows) should be cleaned for a particular application or system component.

When BleachBit starts, it scans specific directories for these XML files. These directories typically include:

*   A system-wide directory where BleachBit installs its default cleaners.
*   A user-specific directory where custom cleaners can be added.

Each XML file describes one or more cleaning operations. When you select an option in the BleachBit interface (e.g., "Firefox - Cache"), BleachBit executes the actions defined in the corresponding XML definition.

## Anatomy of a BleachBit XML Cleaner File

A BleachBit XML file has a specific structure. Here's a simplified overview of common elements:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<cleaner id="my_application_cleaner">
    <label>My Application Cleaner</label>
    <description>Cleans temporary files and cache for My Application.</description>
    <version>1.0</version>
    <icon>myapplication.png</icon> <!-- Optional -->

    <option id="cache">
        <label>Cache Files</label>
        <description>Removes cached data.</description>
        <action command="delete" path="%AppData%\MyApplication\Cache"/>
        <action command="delete" path="%LocalAppData%\MyApplication\Temp\*" recurse="true"/>
    </option>

    <option id="logs">
        <label>Log Files</label>
        <description>Deletes old log files.</description>
        <action command="delete" path="%ProgramData%\MyApplication\Logs\*.log"/>
    </option>

    <!-- Add more options as needed -->

</cleaner>
```

### Key XML Elements:

*   **`<cleaner>`:** The root element for a cleaner definition.
    *   `id`: A unique identifier for the cleaner (e.g., `firefox`, `nvidia_cache`).
*   **`<label>` (under `<cleaner>`):** The name of the application or group of cleaners as it will appear in the BleachBit UI's left pane.
*   **`<description>` (under `<cleaner>`):** A brief description of what this set of cleaners does.
*   **`<version>`:** The version of this cleaner definition file.
*   **`<icon>` (optional):** Specifies an icon to be displayed next to the cleaner in the UI. Icons are typically placed in a subfolder (e.g., `cleaners/icons/`).
*   **`<option>`:** Defines a specific cleaning task that the user can select (e.g., "Cache", "History", "Cookies").
    *   `id`: A unique identifier for this specific option within the cleaner (e.g., `cache`, `logs`).
*   **`<label>` (under `<option>`):** The text displayed for this checkbox option in the BleachBit UI.
*   **`<description>` (under `<option>`):** A more detailed description of what this specific option does, often shown as a tooltip.
*   **`<action>`:** Specifies the actual cleaning operation to perform.
    *   `command`: The type of action. Common commands include:
        *   `delete`: Deletes files or folders.
        *   `wipe`: Securely deletes files (overwrites them before deletion).
        *   `regkey`: (Windows-specific) Deletes a registry key.
        *   `regval`: (Windows-specific) Deletes a registry value.
    *   `path`: The path to the file, folder, or registry key. Environment variables (like `%AppData%`, `%LocalAppData%`, `%UserProfile%`, `%SystemRoot%`) can be used for portability.
        *   Wildcards (`*`, `?`) can be used in file paths.
    *   `recurse="true"` (for `delete` command on folders): Indicates that the deletion should include all subfolders and files.
    *   `filetype="wildcards"` or `filetype="regex"`: Specifies how the `path` should be interpreted for matching files.

### Variables and Paths

BleachBit supports various environment variables to make paths more generic across different systems and user profiles. Some common ones include:

*   `%AppData%`: User's Application Data folder (e.g., `C:\Users\Username\AppData\Roaming`)
*   `%LocalAppData%`: User's Local Application Data folder (e.g., `C:\Users\Username\AppData\Local`)
*   `%UserProfile%`: User's profile directory (e.g., `C:\Users\Username`)
*   `%ProgramFiles%`: Program Files directory (e.g., `C:\Program Files` or `C:\Program Files (x86)`)
*   `%WinDir%` or `%SystemRoot%`: Windows directory (e.g., `C:\Windows`)
*   `%Temp%`: User's temporary files folder.

### Creating Your Own Cleaners

1.  **Identify Targets:** Determine what files, folders, or registry entries an application creates that can be safely deleted (e.g., temporary files, cache, logs, history).
2.  **Research Paths:** Find the exact locations of these items. Tools like Process Monitor (ProcMon) from Sysinternals can be helpful to see what files an application accesses.
3.  **Write the XML:** Create an XML file following the structure described above.
4.  **Test Thoroughly:** This is crucial! Test your cleaner on a non-critical system or a virtual machine first. Incorrectly defined cleaners can potentially delete important system files or user data.
    *   Use BleachBit's "Preview" mode to see what files would be deleted before actually deleting them.

By understanding this structure, you can create your own custom cleaners to extend BleachBit's capabilities or contribute to projects like this one.

For more detailed information, refer to the official BleachBit documentation on [CleanerML](https://docs.bleachbit.org/cleanerml/CleanerML/).