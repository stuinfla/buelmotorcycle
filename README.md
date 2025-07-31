# Buell ECM Real-Time Web Dashboard

This project is a modern, web-based diagnostic tool that provides a real-time "Digital Cockpit" for Buell motorcycles. It uses a Python FastAPI backend with a WebSocket to stream live or simulated engine data to a sleek, responsive frontend featuring animated gauges.

## Key Features

- **Real-Time Gauges**: Displays RPM, Engine Temperature, and Battery Voltage on beautiful, responsive gauges powered by the CanvasGauges.js library.
- **Modern "Digital Cockpit" UI**: A clean, dark-themed interface with the "Orbitron" font for a futuristic, digital feel.
- **High-Performance Backend**: Built with FastAPI for asynchronous, high-speed data streaming via WebSockets.
- **"Connection-Ready" Architecture**: The application intelligently attempts to connect to a real ECM but gracefully falls back to a high-quality simulation if no live data source is available.
- **Fully Self-Contained**: All necessary assets are served locally, requiring no external CDN dependencies at runtime.
- **Cloud-Ready**: Includes a `Procfile` and `requirements.txt` for seamless one-click deployment on platforms like Railway.app or Heroku.

## Architectural Overview

The application is composed of three main components: the frontend, the backend, and the ECM data protocol.

### 1. Frontend

The frontend is a single-page application built with pure HTML, CSS, and JavaScript for maximum portability and performance.

- **`frontend/index.html`**: The main application file containing the structure for the gauges and the client-side JavaScript.
- **`frontend/js/gauge.min.js`**: A local copy of the excellent [CanvasGauges](https://canvas-gauges.com/) library used to render the gauges.
- **Styling**: Custom CSS provides the dark theme, flexbox layout for responsiveness, and imports the "Orbitron" font from Google Fonts.
- **Communication**: A WebSocket client connects to the backend at `ws://<host>/ws`. It listens for incoming JSON messages and updates the value of each gauge accordingly, creating the smooth animation.

### 2. Backend

The backend is powered by FastAPI, a modern, high-performance Python web framework.

- **`main.py`**: The heart of the application. It performs three key functions:
    1.  **Serves Static Files**: It mounts the `frontend` directory, making `index.html` and all its assets available to the browser.
    2.  **Manages the WebSocket**: It provides the `/ws` endpoint that the frontend connects to.
    3.  **Contains the Intelligent Engine**: It houses the core logic for providing either real or simulated data.

- **Data Handling Logic**: Inside a continuous loop, the backend first calls the `get_real_ecm_data()` function. 
    - If this function returns a real data packet, it is parsed and sent to the frontend.
    - If the function returns `None` (e.g., a motorcycle is not connected), the backend generates and sends a realistic, simulated data packet instead. This ensures the application is always functional for demonstration.

### 3. ECM Data Protocol

- **`ecm_protocol.py`**: This file contains the logic for understanding the data coming from the motorcycle.
    - **`BUEGB_RT_MAP`**: A Python dictionary that serves as a memory map for a standard 107-byte Buell ECM real-time data packet. It defines the offset, size, and scaling factor for each engine variable.
    - **`ECM` Class**: A parser that takes a raw data packet and, using the map, translates it into a human-readable dictionary of key-value pairs (e.g., `{'RPM': 1200, 'TE': 90.0, ...}`).

## Getting Started

### Prerequisites
- Python 3.8+
- Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/stuinfla/buelmotorcycle.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd buelmotorcycle
    ```
3.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running Locally

1.  **Start the application:**
    ```bash
    python3 manage.py
    ```
2.  This single command will start the server and automatically open the application in your default web browser.

## Deployment

This application is ready for cloud deployment. The `Procfile` is configured to use `gunicorn` as a production-grade web server. 

To deploy:
1.  Create an account on a platform like [Railway.app](https://railway.app).
2.  Create a new project and choose to deploy from a GitHub repository.
3.  Select your `stuinfla/buelmotorcycle` repository.
4.  The platform will automatically read the `Procfile`, install the dependencies from `requirements.txt`, and launch the application. You will be provided with a public URL to access your live dashboard.

## Connecting to a Real ECM

The application is **"connection-ready."** To switch from the placeholder data to a live feed from your motorcycle, you only need to edit one function:

1.  Open the `main.py` file.
2.  Find the function `get_real_ecm_data()`.
3.  Inside the `try` block, replace the placeholder code with your actual hardware connection logic (e.g., using `pySerial` or `bleak` to connect to your USB adapter or Bluetooth dongle).
4.  Your custom code should return the raw 107-byte data packet from the ECM as a `bytearray`.
5.  Once you save the file and push the changes to GitHub, your live deployment will automatically update to use the real data feed.

## Future Development: Mobile App Conversion

To evolve this tool into a truly portable diagnostic utility, the next logical step is to convert it into a sideloadable mobile application for Android and iOS. A complete, phase-by-phase project plan has been documented to guide this process.

**For the detailed plan, please see [MOBILE_STRATEGY.md](./MOBILE_STRATEGY.md).**

## Acknowledgements and Credit

This project was developed as a collaborative effort and was heavily inspired by the foundational work and deep ECM protocol knowledge from an original open-source repository. Full credit and sincere thanks are given to the original author for providing the initial framework and insights that made this project possible. This dashboard aims to extend that work by providing a modern web interface and a robust, easily deployable architecture.
