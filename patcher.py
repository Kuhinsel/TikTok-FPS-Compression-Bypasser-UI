#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pymediainfo import MediaInfo
import sys

def patch_atom(atom_name, data, scale_factor=None):
    """
    Modifies the 'mvhd' or 'mdhd' atoms inside the MP4 file to adjust
    the timescale and duration, allowing manipulation of video speed/fps.
    """
    count = 0
    start = 0
    atom_bytes = atom_name.encode('utf-8')

    while True:
        found = data.find(atom_bytes, start)
        if found == -1:
            break

        header_offset = found - 4
        if header_offset < 0:
            start = found + 4
            continue

        box_size = int.from_bytes(data[header_offset:header_offset+4], 'big')
        if box_size < 8:
            start = found + 4
            continue

        version = data[header_offset + 8]

        if version == 0:
            timescale_offset = header_offset + 20
            duration_offset = header_offset + 24
            if duration_offset + 4 > header_offset + box_size:
                start = found + 4
                continue

            old_timescale = int.from_bytes(data[timescale_offset:timescale_offset+4], 'big')
            old_duration = int.from_bytes(data[duration_offset:duration_offset+4], 'big')

            chosen_scale = scale_factor or (30000 / old_timescale)
            new_timescale = int(old_timescale * chosen_scale)
            new_duration = int(old_duration * chosen_scale)

            data[timescale_offset:timescale_offset+4] = new_timescale.to_bytes(4, 'big')
            data[duration_offset:duration_offset+4] = new_duration.to_bytes(4, 'big')

            print(f"Patched {atom_name}: timescale {old_timescale}->{new_timescale}, duration {old_duration}->{new_duration}")
            count += 1

        elif version == 1:
            timescale_offset = header_offset + 28
            duration_offset = header_offset + 32
            if duration_offset + 8 > header_offset + box_size:
                start = found + 4
                continue

            old_timescale = int.from_bytes(data[timescale_offset:timescale_offset+4], 'big')
            old_duration = int.from_bytes(data[duration_offset:duration_offset+8], 'big')

            chosen_scale = scale_factor or (30000 / old_timescale)
            new_timescale = int(old_timescale * chosen_scale)
            new_duration = int(old_duration * chosen_scale)

            data[timescale_offset:timescale_offset+4] = new_timescale.to_bytes(4, 'big')
            data[duration_offset:duration_offset+8] = new_duration.to_bytes(8, 'big')

            print(f"Patched {atom_name}: timescale {old_timescale}->{new_timescale}, duration {old_duration}->{new_duration}")
            count += 1
        else:
            print(f"Found {atom_name} with unknown version {version}; skipping.")

        start = found + 4

    return count


def patch_mp4(input_filename, output_filename, scale_factor=None):
    """
    Opens an MP4 file, modifies the 'mvhd' and 'mdhd' atoms to adjust fps/timescale,
    and saves the modified file.
    """
    with open(input_filename, 'rb') as f:
        data = bytearray(f.read())

    patched_mvhd = patch_atom("mvhd", data, scale_factor)
    patched_mdhd = patch_atom("mdhd", data, scale_factor)

    total_patched = patched_mvhd + patched_mdhd
    print(f"\nTotal patched atoms: {total_patched}")

    with open(output_filename, 'wb') as f:
        f.write(data)

    print(f"Patched file written to: {output_filename}")


def get_input_fps(file_path):
    media_info = MediaInfo.parse(file_path)
    for track in media_info.tracks:
        if track.track_type == "Video":
            try:
                return float(track.frame_rate)
            except:
                continue
    return None


class MP4PatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok FPS Bypasser")

        # Input file
        tk.Label(root, text="Input MP4 File:").grid(row=0, column=0, sticky="e")
        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5)

        # Output folder
        tk.Label(root, text="Output Folder:").grid(row=1, column=0, sticky="e")
        self.output_entry = tk.Entry(root, width=50)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5)

        # Scale factor
        tk.Label(root, text="Scale Factor:").grid(row=2, column=0, sticky="e")
        self.scale_entry = tk.Entry(root, width=10)
        self.scale_entry.grid(row=2, column=1, sticky="w", padx=5)
        self.scale_entry.insert(0, "1")
        tk.Label(root, text="e.g., 0.5 = half FPS, 2 = double FPS").grid(row=2, column=1, sticky="e")

        # FPS display
        self.fps_label = tk.Label(root, text="Input FPS: - | Output FPS: -", font=("Arial", 12))
        self.fps_label.grid(row=3, column=1, pady=10)

        # Warning display
        self.warning_label = tk.Label(root, text="", font=("Arial", 12))
        self.warning_label.grid(row=4, column=1, pady=0)

        # Patch button
        tk.Button(root, text="Patch MP4", command=self.patch_file, bg="lightblue").grid(row=5, column=1, pady=5)

        # Update output FPS when scale changes
        self.scale_entry.bind("<KeyRelease>", lambda e: self.update_fps_display())

    def browse_input(self):
        filename = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if filename:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, filename)
            self.update_fps_display()

    def browse_output(self):
        foldername = filedialog.askdirectory()
        if foldername:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, foldername)

    def update_fps_display(self):
        input_file = self.input_entry.get()
        scale_factor = self.scale_entry.get()
        if not input_file or not os.path.exists(input_file):
            self.fps_label.config(text="Input FPS: 30 | Output FPS: -", fg="black")
            return

        try:
            scale = float(scale_factor)
        except ValueError:
            scale = 1

        input_fps = get_input_fps(input_file)
        if input_fps is None:
            self.fps_label.config(text="Could not read input FPS", fg="black")
            return

        output_fps = input_fps * scale
        # Default color
        color = "black"
        # FPS part
        self.fps_label.config(
            text=f"Input FPS: {input_fps:.1f} (30 FPS on Tiktok) | Output FPS: {output_fps:.1f} ({30*scale} FPS on Tiktok)"
        )

        # Warning part
        if output_fps > 120:
            self.warning_label.config(text="(May lag on some devices)", fg="gray")
        # Warning part
        elif output_fps > 240:
            self.warning_label.config(text="(Will lag on most devices)", fg="gray")
        else:
            self.warning_label.config(text="")


        # Color logic
        if scale <= 1:
            color = "black"
        elif scale <= 3:
            color = "green"
        elif scale <= 7:
            color = "orange"
        elif scale >= 8:
            color = "red"
        else:
            color = "black"
        self.fps_label.config(fg=color)

    def patch_file(self):
        input_file = self.input_entry.get()
        output_folder = self.output_entry.get()
        scale_factor = self.scale_entry.get()

        if not input_file or not output_folder:
            messagebox.showerror("Error", "Please select input file and output folder.")
            return

        try:
            scale = float(scale_factor)
        except ValueError:
            scale = None

        output_file = os.path.join(output_folder, os.path.basename(input_file[:-4] + "_patched.mp4"))
        try:
            patch_mp4(input_file, output_file, scale_factor=scale)
            messagebox.showinfo("Success", f"File patched successfully:\n{output_file}")
            self.update_fps_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to patch MP4:\n{e}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        # CLI mode
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        factor = None
        if len(sys.argv) > 3:
            try:
                factor = float(sys.argv[3])
            except ValueError:
                print("Invalid scale factor, using automatic adjustment.")
        patch_mp4(input_file, output_file, scale_factor=factor)
    else:
        # GUI mode
        root = tk.Tk()
        app = MP4PatcherApp(root)
        root.mainloop()
