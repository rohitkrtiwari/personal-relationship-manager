import subprocess
import threading
import time
from pynput import keyboard
import psutil

OVERLAY_CMD = ["python3", "open_overlay.py"]
overlay_process = None
last_ping = time.time()

# ---- Process Management ----
def is_process_alive(process):
    try:
        return process and process.poll() is None
    except Exception:
        return False

def launch_overlay():
    global overlay_process, last_ping

    if is_process_alive(overlay_process):
        print("Overlay already running.")
        return

    print("Launching overlay...")
    overlay_process = subprocess.Popen(OVERLAY_CMD)
    last_ping = time.time()

def kill_overlay():
    global overlay_process
    if is_process_alive(overlay_process):
        print(f"Killing overlay with PID {overlay_process.pid}")
        overlay_process.terminate()
        overlay_process.wait()
    overlay_process = None

# ---- Inactivity Monitor ----
def inactivity_monitor():
    global last_ping
    while True:
        time.sleep(1)
        if is_process_alive(overlay_process):
            if time.time() - last_ping > 5:
                print("Inactivity detected. Closing overlay.")
                kill_overlay()

# ---- Keyboard Listener ----
ctrl_pressed = False

def on_press(key):
    global ctrl_pressed
    try:
        if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            ctrl_pressed = True
        elif hasattr(key, "char") and key.char == 'k' and ctrl_pressed:
            launch_overlay()
    except Exception:
        pass

def on_release(key):
    global ctrl_pressed
    try:
        if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            ctrl_pressed = False
        elif key == keyboard.Key.esc:
            kill_overlay()
            return True  # Stop listener
    except Exception:
        pass

# ---- Flask Ping Receiver ----
def ping_watcher():
    from flask import Flask, request
    app = Flask(__name__)

    @app.route("/ping", methods=["POST"])
    def ping():
        global last_ping
        last_ping = time.time()
        return "", 204

    app.run(port=5050, debug=False)

# ---- Main Entry ----
if __name__ == "__main__":
    threading.Thread(target=inactivity_monitor, daemon=True).start()
    threading.Thread(target=ping_watcher, daemon=True).start()

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
