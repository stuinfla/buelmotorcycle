import uvicorn
import webbrowser
import time
import threading

def open_browser():
    """Waits for a moment and then opens the web browser."""
    time.sleep(2) # Give the server a moment to start
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    print("--- Starting Buell ECM Web Dashboard ---")
    print("Server will be available at: http://127.0.0.1:8000")
    print("Opening browser automatically...")
    
    # Run the browser-opening function in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Start the Uvicorn server
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
