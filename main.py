import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment
import subprocess

def load_audio(file_path):
    try:
        return AudioSegment.from_file(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load audio file: {e}")
        return None

def compress_audio(audio, input_path, output_path, bitrate="64k"):
    try:
        command = [
            "ffmpeg",
            "-i", input_path,
            "-b:a", bitrate,
            output_path
        ]
        subprocess.run(command, check=True)
        return AudioSegment.from_file(output_path)
    except Exception as e:
        messagebox.showerror("Error", f"Audio compression failed: {e}")
        return None

def main():
    def show_coming_soon(feature):
        messagebox.showinfo("Coming Soon", f"{feature} feature is coming soon!")

    def process_audio(selected_option):
        if selected_option == "Add Effects":
            show_coming_soon("Add Effects")
            return
        
        if selected_option == "Speed Adjustment":
            show_coming_soon("Speed Adjustment")
            return

        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=(
                ("Audio Files", "*.mp3 *.wav *.ogg *.flac"),
                ("All Files", "*.*")
            )
        )
        if not file_path:
            return

        audio = load_audio(file_path)
        if audio is None:
            return

        save_path = filedialog.asksaveasfilename(
            title="Save Compressed Audio",
            defaultextension=".mp3",
            filetypes=(
                ("MP3 Files", "*.mp3"),
                ("All Files", "*.*")
            )
        )
        if save_path:
            processed_audio = compress_audio(audio, file_path, save_path, bitrate="64k")
            if processed_audio:
                messagebox.showinfo("Success", "Audio compressed and saved successfully!")

    root = tk.Tk()
    root.title("Audio Processing Tool")
    root.geometry("400x400")

    tk.Label(root, text="Audio Processing Tool", font=("Helvetica", 16)).pack(pady=30)

    buttons = [
        ("Audio Compression", "Compress your audio files"),
        ("Add Effects", "Coming soon"),
        ("Speed Adjustment", "Coming soon")
    ]

    for text, tooltip in buttons:
        btn = tk.Button(root, text=text, 
                        command=lambda t=text: process_audio(t), 
                        font=("Helvetica", 12),
                        width=20)
        btn.pack(pady=10)
        tk.Label(root, text=tooltip, font=("Helvetica", 10)).pack()

    root.mainloop()

if __name__ == "__main__":
    main()
