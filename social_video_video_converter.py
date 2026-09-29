import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy import VideoFileClip
import os

def choose_video():
    file_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv")]
    )
    if file_path:
        lbl_file.config(text=os.path.basename(file_path))
        global selected_video
        selected_video = file_path

def resize_video():
    if not selected_video:
        messagebox.showerror("Error", "Please select a video file first.")
        return
        
    lbl_status.config(text="Processing video... This might take a minute...", fg="orange")
    root.update()
    
    try:
        clip = VideoFileClip(selected_video)
        w, h = clip.size
        
        mode = var_mode.get()
        
        if mode == "vertical":
            new_w = int(h * (9 / 16))
            if new_w > w:
                new_w = w
                new_h = int(w * (16 / 9))
                # WINDOWS COMPATIBILITY FIX: Force the dimensions to be even numbers
                new_h = new_h if new_h % 2 == 0 else new_h - 1
                x1, y1 = 0, (h - new_h) // 2
                x2, y2 = w, y1 + new_h
            else:
                new_w = new_w if new_w % 2 == 0 else new_w - 1
                x1, y1 = (w - new_w) // 2, 0
                x2, y2 = x1 + new_w, h
        else:
            side = min(w, h)
            side = side if side % 2 == 0 else side - 1
            x1, y1 = (w - side) // 2, (h - side) // 2
            x2, y2 = x1 + side, y1 + side
            
        cropped_clip = clip.cropped(x1=x1, y1=y1, x2=x2, y2=y2)
        
        save_path = filedialog.asksaveasfilename(
            title="Save Resized Video",
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4")]
        )
        
        if save_path:
            cropped_clip.write_videofile(
                save_path, 
                codec="libx264", 
                audio_codec="aac",
                temp_audiofile="temp-audio.m4a",
                remove_temp=True
            )
            lbl_status.config(text="Done! Video saved successfully.", fg="green")
            messagebox.showinfo("Success", "Video resized perfectly!")
        else:
            lbl_status.config(text="Cancelled.", fg="gray")
            
        clip.close()
        cropped_clip.close()
        
    except Exception as e:
        lbl_status.config(text="Error occurred.", fg="red")
        messagebox.showerror("Error", f"Failed to resize video:\n{str(e)}")

# UI Setup
root = tk.Tk()
root.title("Social Media Video Resizer")
root.geometry("450x350")

selected_video = ""

btn_browse = tk.Button(root, text="Choose Video File", command=choose_video, font=("Arial", 11))
btn_browse.pack(pady=20)

lbl_file = tk.Label(root, text="No video selected", fg="gray", font=("Arial", 10, "italic"))
lbl_file.pack()

frame_options = tk.LabelFrame(root, text=" Target Format ", padx=10, pady=10)
frame_options.pack(pady=20, fill="x", padx=20)

var_mode = tk.StringVar(value="vertical")

rb_vertical = tk.Radiobutton(frame_options, text="Vertical 9:16 (TikTok, Shorts, Reels)", variable=var_mode, value="vertical")
rb_vertical.pack(anchor="w", pady=2)

rb_square = tk.Radiobutton(frame_options, text="Square 1:1 (Instagram Feed / Posts)", variable=var_mode, value="square")
rb_square.pack(anchor="w", pady=2)

btn_run = tk.Button(root, text="Crop & Export Video", command=resize_video, bg="blue", fg="white", font=("Arial", 12, "bold"))
btn_run.pack(pady=20)

lbl_status = tk.Label(root, text="", font=("Arial", 11, "bold"))
lbl_status.pack()

root.mainloop()
