import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def choose_file():
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac *.m4a")]
    )
    if file_path:
        lbl_file.config(text=os.path.basename(file_path))
        global selected_file
        selected_file = file_path

def process_audio():
    if not selected_file:
        messagebox.showerror("Error", "Please select a file first.")
        return
    
    # Get values from sliders
    try:
        min_silence = int(slider_len.get())
        silence_thresh = int(slider_thresh.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid settings.")
        return

    lbl_status.config(text="Processing... Please wait...", fg="orange")
    root.update()

    try:
        # Load the file
        file_ext = os.path.splitext(selected_file)[1][1:]
        sound = AudioSegment.from_file(selected_file, format=file_ext)
        
        # Split on silence and glue back together
        chunks = split_on_silence(
            sound,
            min_silence_len=min_silence,
            silence_thresh=silence_thresh,
            keep_silence=100 # keeps 100ms padding so cuts sound natural
        )
        
        if not chunks:
            messagebox.showwarning("Warning", "The settings wiped out the entire file. Try turning down the threshold.")
            lbl_status.config(text="Failed.", fg="red")
            return
            
        combined = sum(chunks)
        
        # Save output
        save_path = filedialog.asksaveasfilename(
            title="Save Cleaned Audio",
            defaultextension=".mp3",
            filetypes=[("MP3 File", "*.mp3"), ("WAV File", "*.wav")]
        )
        
        if save_path:
            save_ext = os.path.splitext(save_path)[1][1:]
            combined.export(save_path, format=save_ext)
            lbl_status.config(text="Done! File saved successfully.", fg="green")
            messagebox.showinfo("Success", "Silence removed completely.")
        else:
            lbl_status.config(text="Cancelled.", fg="gray")
            
    except Exception as e:
        lbl_status.config(text="Error occurred.", fg="red")
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

# UI Setup
root = tk.Tk()
root.title("Silence Stripper for Creators")
root.geometry("450x400")

selected_file = ""

# File Picker
btn_browse = tk.Button(root, text="Choose Audio File", command=choose_file, font=("Arial", 11))
btn_browse.pack(pady=20)

lbl_file = tk.Label(root, text="No file selected", fg="gray", font=("Arial", 10, "italic"))
lbl_file.pack()

# Settings Frame
frame_settings = tk.LabelFrame(root, text=" Tuning Settings ", padx=10, pady=10)
frame_settings.pack(pady=20, fill="x", padx=20)

# Silence Duration Slider
tk.Label(frame_settings, text="Minimum silence length (ms):").pack(anchor="w")
slider_len = tk.Scale(frame_settings, from_=100, to=2000, orient="horizontal")
slider_len.set(500) # defaults to half a second
slider_len.pack(fill="x", pady=5)

# Silence Threshold Slider
tk.Label(frame_settings, text="Silence threshold (dBFS - lower means quieter):").pack(anchor="w")
slider_thresh = tk.Scale(frame_settings, from_=-60, to=-10, orient="horizontal")
slider_thresh.set(-40) # standard background noise level
slider_thresh.pack(fill="x", pady=5)

# Process Button
btn_run = tk.Button(root, text="Strip Silence & Export", command=process_audio, bg="green", fg="white", font=("Arial", 12, "bold"))
btn_run.pack(pady=20)

lbl_status = tk.Label(root, text="", font=("Arial", 11, "bold"))
lbl_status.pack()

root.mainloop()
