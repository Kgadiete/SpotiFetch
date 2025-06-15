#SpotiFetch

SpotiFetch is a command-line tool to download Spotify playlists as MP3 files using metadata fetched from the Spotify Web API and audio from YouTube.

## Features
- Clean output with progress tracking per track.
- Uses `yt-dlp` to fetch audio.
- Converts audio to high-quality MP3 using `ffmpeg`.
- Graceful Ctrl+C support.
- Skips files that already exist.

## Requirements
- Python 3.7+
- `ffmpeg` must be installed and added to your system PATH

## Installation
```bash
git clone https://github.com/yourusername/SpotiFetch.git
cd SpotiFetch
pip install -r requirements.txt