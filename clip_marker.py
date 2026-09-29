import tkinter as tk
from tkinter import messagebox
import keyboard
import time
from datetime import datetime
import os

class StreamDeck:
    def __init__(self, root):
        self.root = root
        self.root.title("Streamer Clip Deck")
        self.root.geometry("400x350")
        
        self.is_recording = False
        self.start_time = None
        self.marker_file = "stream_markers.txt"
        
        self.lbl_info = tk.Label(
            root, 
            text="Press 'Start Stream' to track time.\nHotkey to log a clip marker: F8 (or use button)", 
            font=("Arial", 11), 
            pady=15
        )
        self.lbl_info.pack()
        
        self.btn_toggle = tk.Button(
            root, 
            text="Start Stream / Recording", 
            command=self.toggle_stream, 
            bg="green", 
            fg="white", 
            font=("Arial", 12, "bold"),
            pady=5
        )
        self.btn_toggle.pack(pady=5)

        # FIXED: Added a physical button you can click to drop markers instantly
        self.btn_marker = tk.Button(
            root,
            text="🎯 DROP CLIP MARKER",
            command=self.add_marker,
            bg="blue",
            fg="white",
            font=("Arial", 11, "bold"),
            pady=5,
            state="disabled" # Starts off until stream goes live
        )
        self.btn_marker.pack(pady=10)
        
        self.lbl_status = tk.Label(root, text="Status: Idle", fg="gray", font=("Arial", 11, "bold"))
        self.lbl_status.pack(pady=5)
        
        self.txt_log = tk.Text(root, height=6, width=45, state="disabled")
        self.txt_log.pack(pady=10)

        # FIXED: Changed 'F8' to lowercase 'f8' for better library mapping
        try:
            keyboard.add_hotkey('f8', self.add_marker)
        except Exception:
            pass # Fallback to button if global keyboard hook fails

    def toggle_stream(self):
        if not self.is_recording:
            self.is_recording = True
            self.start_time = time.time()
            self.btn_toggle.config(text="Stop Stream", bg="red")
            self.btn_marker.config(state="normal") # Enable the manual marker button
            self.lbl_status.config(text="Status: Live & Tracking...", fg="green")
            self.log_message(f"--- Stream Started at {datetime.now().strftime('%H:%M:%S')} ---")
            
            with open(self.marker_file, "a") as f:
                f.write(f"\n=== NEW SESSION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
        else:
            self.is_recording = False
            self.btn_toggle.config(text="Start Stream", bg="green")
            self.btn_marker.config(state="disabled") # Disable button when idle
            self.lbl_status.config(text="Status: Idle", fg="gray")
            self.log_message("--- Stream Stopped ---")

    def add_marker(self):
        if not self.is_recording:
            return
            
        elapsed_seconds = int(time.time() - self.start_time)
        
        hours = elapsed_seconds // 3600
        minutes = (elapsed_seconds % 3600) // 60
        seconds = elapsed_seconds % 60
        timestamp = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        with open(self.marker_file, "a") as f:
            f.write(f"Clip Marker at -> {timestamp}\n")
            
        self.log_message(f"Marker saved at {timestamp}")

    def log_message(self, msg):
        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, msg + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = StreamDeck(root)
    
    def on_closing():
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
