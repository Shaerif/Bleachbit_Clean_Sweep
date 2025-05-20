# Bleachbit Clean Sweep

## Overview

Bleachbit Clean Sweep is a project dedicated to providing custom cleaner definitions (XML files) for BleachBit, a powerful open-source system cleaner. This project aims to extend BleachBit's cleaning capabilities by targeting specific applications and system areas not covered by default cleaners.

Our goal is to help users reclaim disk space, protect their privacy, and maintain system performance by thoroughly removing unnecessary files.

## Features

*   **Custom Cleaners:** A growing collection of XML files for various applications and system components.
*   **Community Driven:** Contributions and suggestions for new cleaners are welcome.
*   **Easy to Use:** Simple instructions on how to add these custom cleaners to your BleachBit installation.

## Getting Started

To use the custom cleaners from this project:

1.  **Download BleachBit:** If you haven't already, download and install BleachBit from [bleachbit.org](https://www.bleachbit.org/).
2.  **Download Cleaners:** The custom cleaner XML files are located in the `cleaners` directory of this repository. Download the specific `.xml` files for the applications or system areas you wish to clean.
    *   For example, you can find `cleaners/nvidia.xml` for NVIDIA-related cleanup.
3.  **Import Cleaners:** You have two main ways to add these cleaners to BleachBit:
    *   **Manual Import:** Follow the instructions in <mcfile name="IMPORT_XML.md" path="d:\Projects\Bleachbit_Clean_Sweep\docs\IMPORT_XML.md"></mcfile> to import the XML files through the BleachBit interface or by manually placing them in the correct folder.
    *   **Automated Deployment (Windows PowerShell):** For Windows users, a PowerShell script <mcfile name="deploy_cleaners.ps1" path="d:\Projects\Bleachbit_Clean_Sweep\deploy_cleaners.ps1"></mcfile> is provided in the project root. This script will automatically copy all `.xml` files from the `cleaners` directory of this project to your user-specific BleachBit cleaners folder (`%AppData%\BleachBit\cleaners`).
        *   To use it: Right-click on `deploy_cleaners.ps1` and select "Run with PowerShell".
        *   You might need to adjust your PowerShell execution policy if scripts are disabled. (e.g., `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`)

### A Note on Paths and OS Versions

BleachBit cleaner XML files are designed to be portable across different Windows installations (like Windows 10 and Windows 11) and user profiles. They achieve this by using standard Windows environment variables (e.g., `%AppData%`, `%LocalAppData%`, `%ProgramFiles%`, `%WinDir%`). These variables are automatically resolved to the correct paths on the computer where BleachBit is running. Therefore, the XML files in this project generally do not need to be modified after being placed in the BleachBit cleaners directory.

## Contributing

We welcome contributions! If you have created a new cleaner or improved an existing one, please feel free to submit a pull request. See `CONTRIBUTING.md` (to be created) for more details.

## License

This project is licensed under the [MIT License](LICENSE) (to be created).

## Recent Updates

* **GUI Tool:** Added a simple GUI tool `cleaner_manager_gui.py` to help users manage custom BleachBit cleaners.
* **Requirements File:** Created `requirements.txt` to list dependencies for the GUI tool.

## [Updated] - 2025-05-20