import tkinter as tk
import requests
import threading
import time  # Added missing import

def send_ping():
    def ping_loop():
        while True:
            try:
                requests.post("http://127.0.0.1:5050/ping")
            except:
                pass
            time.sleep(1)
    threading.Thread(target=ping_loop, daemon=True).start()

def on_escape(event):
    root.destroy()

root = tk.Tk()
root.withdraw()  # Hide main root window

overlay = tk.Toplevel()
overlay.overrideredirect(True)
overlay.attributes("-topmost", True)
overlay.geometry("500x80+700+300")  # Width, Height, X, Y

# Semi-transparent dark background with glow effect
overlay.configure(bg="#000000")
overlay.wm_attributes("-alpha", 0.8)

# Centered frame for input
frame = tk.Frame(overlay, bg="#222222", padx=20, pady=20)
frame.pack(expand=True, fill="both")

entry = tk.Entry(frame, font=("Helvetica", 20), width=40, 
                 bg="#333333", fg="white", insertbackground="white")
entry.pack()

# Improved focus handling
def set_focus():
    entry.focus_set()
    overlay.lift()
    overlay.after(100, set_focus)  # Continuously ensure focus

overlay.after(100, set_focus)
overlay.bind("<Escape>", on_escape)

# Don't use grab_set() as it can be too restrictive
# overlay.grab_set()  # Removed this line

send_ping()
root.mainloop()