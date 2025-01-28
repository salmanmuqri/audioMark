import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pydub import AudioSegment, effects
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

def apply_effect(audio, effect):
    try:
        if effect == "Bass Boost":
            return audio.low_pass_filter(200).apply_gain(5)
        elif effect == "Reverb":
            return effects.normalize(audio + audio.reverse())
        elif effect == "Slow Down":
            return audio.set_frame_rate(int(audio.frame_rate * 0.75))
        else:
            messagebox.showinfo("Error", "Unknown effect selected.")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to apply effect: {e}")
        return None

def main():
    def process_audio(selected_option):
        if selected_option == "Add Effects":
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

            def select_effect():
                selected_effect = effect_var.get()
                save_path = filedialog.asksaveasfilename(
                    title="Save Processed Audio",
                    defaultextension=".mp3",
                    filetypes=(
                        ("MP3 Files", "*.mp3"),
                        ("All Files", "*.*")
                    )
                )
                if save_path:
                    processed_audio = apply_effect(audio, selected_effect)
                    if processed_audio:
                        processed_audio.export(save_path, format="mp3")
                        messagebox.showinfo("Success", "Effect applied and audio saved successfully!")

            effect_window = tk.Toplevel(root)
            effect_window.title("Select Effect")
            effect_window.geometry("300x200")

            tk.Label(effect_window, text="Select an effect to apply:", font=("Helvetica", 12)).pack(pady=10)

            effect_var = tk.StringVar(value="Bass Boost")
            effects_options = ["Bass Boost", "Reverb", "Slow Down"]
            for effect in effects_options:
                tk.Radiobutton(effect_window, text=effect, variable=effect_var, value=effect, font=("Helvetica", 10)).pack(anchor=tk.W)

            tk.Button(effect_window, text="Apply Effect", command=select_effect, font=("Helvetica", 12)).pack(pady=20)

            return

        if selected_option == "Speed Adjustment":
            messagebox.showinfo("Coming Soon", "Speed Adjustment feature is coming soon!")
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
        ("Add Effects", "Add effects like bass boost, reverb, etc."),
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
