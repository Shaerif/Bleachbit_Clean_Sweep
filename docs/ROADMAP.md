# Project Roadmap 🗺️

This document outlines the planned features and improvements for the Bleachbit Clean Sweep project.

## Short-Term Goals (Next 1-3 Months) ⏳

*   **Initial Cleaner Set:**
    *   Develop and test cleaners for popular NVIDIA software components.
    *   Add cleaners for common web browsers (beyond default BleachBit capabilities).
    *   Include cleaners for frequently used utility applications.
*   **Documentation:**
    *   Complete `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, and `LICENSE`.
    *   Finalize `docs/HOW_IT_WORKS.md` explaining BleachBit's mechanism and XML structure.
    *   Create `docs/IMPORT_XML.md` with clear instructions for users.
*   **Basic Testing Framework:**
    *   Establish a manual testing procedure for each new cleaner.
*   **GUI Tool:** Implemented a simple GUI tool for managing custom cleaners.

## Mid-Term Goals (Next 3-6 Months)

*   **Expand Cleaner Library:**
    *   Target a wider range of software categories (e.g., gaming platforms, development tools, multimedia applications).
    *   Research and implement cleaners for system-specific temporary files and caches not covered by default BleachBit.
*   **Community Engagement:**
    *   Set up a clear process for community contributions and suggestions.
    *   Actively seek feedback on existing cleaners and desired new ones.
*   **Enhanced Documentation:**
    *   Provide more detailed explanations for complex cleaners.
    *   Consider creating video tutorials for importing and using custom cleaners.

## Long-Term Goals (6+ Months)

*   **Automated Testing:**
    *   Explore possibilities for automating parts of the cleaner testing process.
*   **Localization:**
    *   If demand exists, consider translating documentation and cleaner descriptions into other languages.
*   **Advanced Cleaner Features:**
    *   Investigate advanced BleachBit features (e.g., Winapp2.ini format compatibility, scripting) for more powerful cleaning options.
*   **Regular Updates:**
    *   Establish a schedule for reviewing and updating existing cleaners to ensure compatibility with new software versions.

## Ideas Under Consideration 🤔

*   A simple GUI tool to help users manage their custom BleachBit cleaners.
*   Integration with popular software update checkers to identify when new cleaner versions might be needed.
*   **BleachBit Backup & Restore:** Implement functionality to backup and restore BleachBit settings, including selected checkboxes for cleaning operations.
*   **Import/Export Checked Options:** Allow users to import and export their preferred cleaning configurations (checked checkboxes).
*   **Auto-Update BleachBit:** ~~Develop a feature to automatically download and update BleachBit to the latest beta or stable versions.~~ Implemented an enhanced auto-update feature for BleachBit. This includes:
    *   Ability to choose between **stable, beta, and unstable (CI builds)** versions for download.
    *   Fetching the latest unstable builds directly from the BleachBit CI server (`https://ci.bleachbit.org/`).
    *   A **debug mode** for the updater script, accessible via a GUI checkbox, to help with troubleshooting.
*   **Portable Version Download:** Add an option to download a portable version of BleachBit.
*   **Download Progress Bar:** Implement a visual progress bar for BleachBit downloads in the updater.
*   **Enhanced Download Visualization & Debugging:** Improve the visual feedback during the download process and expand debugging capabilities for the updater.

## [Updated] - 2025-05-21

This roadmap is a living document and will be updated as the project evolves and based on community feedback.