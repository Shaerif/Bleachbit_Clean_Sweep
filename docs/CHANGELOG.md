# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
 
## [Unreleased] - 2025-05-20
### Added
- Replaced `deploy_cleaners.ps1` with `deploy_cleaners.py` for cross-platform compatibility.
- Added `cleaner_manager_gui.py` for managing custom cleaners.
- Created `requirements.txt` for GUI tool dependencies.

### Date
* 2023-10-12

### Added

*   Initial project structure.
*   `README.md` for project overview.
*   `ROADMAP.md` for future plans.
*   `CHANGELOG.md` to track changes (this file).
*   Created `docs/HOW_IT_WORKS.md` explaining BleachBit's mechanism and XML structure.
*   Created `docs/IMPORT_XML.md` with instructions for importing custom cleaners.
*   Created `cleaners` directory.
*   Added initial `cleaners/nvidia.xml` for NVIDIA software cleanup.
* Replaced `deploy_cleaners.ps1` PowerShell script with `deploy_cleaners.py` Python script for cross-platform compatibility.

### Changed

*   Updated `README.md` with instructions for `deploy_cleaners.ps1` and a note on how BleachBit XMLs handle path differences using environment variables.

*   N/A

### Deprecated

*   N/A

### Removed

*   N/A

### Fixed

*   N/A

### Security

*   N/A

## [0.1.0] - YYYY-MM-DD

### Added

*   First set of custom cleaners (e.g., NVIDIA).
*   Basic documentation.

*(This is a template. Actual versions and changes will be filled in as the project progresses.)*