import asyncio
import json
import random
import struct
import logging
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from whitenoise import WhiteNoise

# Import the ECM protocol definitions
from ecm_protocol import ECM, BUEGB_RT_MAP

# --- FastAPI Application Setup ---
app = FastAPI()

# Get the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Mount WhiteNoise to serve static files from the 'frontend' directory
# This is the production-ready way to handle static assets
app.mount("/", WhiteNoise(directory=BASE_DIR / "frontend", index_file="index.html"), name="static")

# --- Placeholder for Real ECM Data Retrieval ---
def get_real_ecm_data():
    """
    *** THIS IS A PLACEHOLDER FUNCTION ***
    This function should contain the logic to connect to the Buell ECM
    via Bluetooth or serial and return the raw 107-byte data packet.
    
    - If a connection is successful, it should return the `raw_data` (bytearray).
    - If no connection is available, it should return `None`.

    For now, it returns a sample packet to demonstrate functionality.
    """
    try:
        # --- Replace this section with your actual hardware connection logic ---
        # Example: ecm_connection = connect_to_bluetooth_device('XX:XX:XX:XX:XX:XX')
        # raw_data = ecm_connection.read_realtime_packet()
        # return raw_data
        
        # For demonstration, we'll use the sample data from the test harness:
        sample_data = bytearray(107)
        sample_data[11:13] = struct.pack('>H', random.randint(900, 5500)) # RPM
        sample_data[30:32] = struct.pack('>H', random.randint(1200, 1400)) # Engine Temp
        sample_data[28:30] = struct.pack('>H', random.randint(1380, 1450)) # Battery
        return sample_data

    except Exception as e:
        # In a real scenario, this would catch connection errors.
        logging.info(f"Could not connect to real ECM, falling back to simulation. Error: {e}")
        return None

# --- WebSocket Endpoint for Live Data ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logging.info("WebSocket client connected.")
    
    ecm_parser = ECM(BUEGB_RT_MAP)

    try:
        while True:
            data = None
            raw_ecm_data = get_real_ecm_data()

            if raw_ecm_data:
                # If we have real data, parse it
                parsed_data = ecm_parser.parse_realtime_data(raw_ecm_data)
                data = {
                    "RPM": round(parsed_data.get('RPM', 0)),
                    "TE": round(parsed_data.get('TE', 0), 1),
                    "VB": round(parsed_data.get('Bat', 0), 2)
                }
            else:
                # If no real data, fall back to simulation
                rpm = random.randint(800, 1200) + (random.randint(0, 5000) * (random.random() ** 2))
                temp = 60 + (rpm / 7500) * 40 + random.uniform(-2, 2)
                voltage = 14.4 - (rpm / 7500) * 1.2 + random.uniform(-0.1, 0.1)
                data = {
                    "RPM": round(rpm),
                    "TE": round(temp, 1),
                    "VB": round(voltage, 2)
                }

            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        logging.info("WebSocket client disconnected.")
    except Exception as e:
        logging.error(f"An error occurred in the WebSocket endpoint: {e}")

# To run this application:
# uvicorn main:app --reload
