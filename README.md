# TikTok FPS Bypasser (Forked Version)

This project is a fork of [LuisAlves10/TikTok-FPS-Compression-Bypasser](https://github.com/LuisAlves10/TikTok-FPS-Compression-Bypasser) with improvements for GUI usability and FPS display. It allows modifying MP4 files to bypass TikTok's FPS restrictions by patching the `mvhd` and `mdhd` atoms.

---

## Features in This Fork

- Added **GUI mode** with file browsing and output folder selection.
- Displays **input FPS** and **output FPS** in real-time.
- Color-coded FPS warnings:
- Warns dynamically if output FPS may cause lag.
- CLI mode still supported for scripting and automation.

## Installation

1. Clone or download this repository.
2. Install dependencies:

```bash
pip install pymediainfo
```

3. Make sure MediaInfo is installed on your system:
Windows: [Download MediaInfo](https://mediaarea.net/en/MediaInfo/Download/Windows)
Linux (Debian/Ubuntu):
```bash
sudo apt install mediainfo
```
macOS (Homebrew):
```bash
brew install mediainfo
```

## Usage
# GUI Mode
Run without arguments:
```bash
python patcher.py
```

# CLI Mode
```bash
python patch_mp4_gui.py input.mp4 output.mp4 [scale_factor]
```

## License

This project is **open source** and you can use, modify, and contribute freely.
