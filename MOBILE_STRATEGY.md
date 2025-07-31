# Mobile App Conversion Strategy

This document outlines the strategic plan to evolve the Buell ECM Web Dashboard from a web application into a fully sideloadable, native mobile application for Android and iOS using a hybrid app approach.

## Recommended Technology: Capacitor

We will use **Capacitor**, a modern open-source framework, to wrap our existing web frontend in a native shell. This approach allows us to reuse our entire UI codebase while gaining full access to native device features like Bluetooth.

## The Four-Phase Project Plan

### Phase 1: Decouple Frontend & Deploy Backend

*   **Objective**: Prepare the application for a client-server architecture where the mobile app (client) is separate from the backend (server).
*   **Key Tasks**:
    1.  Deploy the current Python/FastAPI backend to a public cloud provider like Railway.app. This will provide a stable, public WebSocket URL (e.g., `wss://your-app-name.railway.app/ws`).
    2.  Modify the `frontend/index.html` file to replace the relative WebSocket URL (`ws://${window.location.host}/ws`) with the new, hardcoded public URL from the deployed backend.
*   **Estimated Time**: 15 - 30 minutes.

### Phase 2: Introduce Capacitor & Set Up Mobile Project

*   **Objective**: Create the foundational structure for the native mobile application.
*   **Prerequisites**: A development machine with Node.js, npm, Android Studio (for Android), and Xcode (for iOS) installed.
*   **Key Tasks**:
    1.  Initialize a new `package.json` file using `npm`.
    2.  Install the Capacitor CLI and its core dependencies.
    3.  Configure Capacitor to use our existing `frontend` directory as the source for its web view.
    4.  Generate the native Android and iOS project folders using the Capacitor CLI.
*   **Estimated Time**: 1 - 2 hours (excluding IDE installation).

### Phase 3: Integrate Native Bluetooth

*   **Objective**: Replace the Python-based data retrieval logic with a native Bluetooth implementation controlled by JavaScript.
*   **Key Tasks**:
    1.  Select and install a suitable Capacitor Bluetooth LE plugin (e.g., `capacitor-community/bluetooth-le`).
    2.  Write new JavaScript code within the frontend to manage the entire Bluetooth lifecycle:
        - Requesting user permissions.
        - Scanning for the Buell ECM's Bluetooth dongle.
        - Establishing a connection.
        - Subscribing to the correct data characteristic.
        - Receiving the raw data packets.
    3.  The JavaScript code will then parse the raw data (using a JS-based version of the logic in `ecm_protocol.py`) and update the gauges.
*   **Estimated Time**: 3 - 5 hours.

### Phase 4: Build, Sign, and Sideload

*   **Objective**: Compile the final, distributable application packages (`.apk` for Android, `.ipa` for iOS).
*   **Key Tasks**:
    1.  Open the generated native projects in Android Studio and Xcode.
    2.  Configure the necessary application identifiers, permissions, and signing certificates.
    3.  Build the release version of the application.
    4.  The resulting files can be directly transferred to a mobile device for installation (sideloading).
*   **Estimated Time**: 1 - 2 hours.

---

This strategic plan provides a clear and actionable roadmap to transform the web dashboard into a powerful, portable mobile utility.
