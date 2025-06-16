# SpotiFetch
SpotiFetch is a command-line tool to download Spotify playlists as MP3 files using metadata fetched from the Spotify Web API and audio from YouTube.


---

## Demonstration-Video
🔗 Need help using SpotiFetch? [Watch this setup video](https://youtu.be/VfHzlrjuaBo)

---

## ⚙️ Features
- Clean per-track output with colored status messages.
- Converts YouTube audio to MP3 via `ffmpeg`.
- Automatically creates folders named after playlists.
- Skips already-downloaded tracks.
- Ctrl+C safe — cancels cleanly.
- No Spotify login needed (uses Client Credentials Flow).

---

## 📦 Requirements
- Python 3.7 or higher
- [`ffmpeg`](https://ffmpeg.org/download.html) installed and added to your system PATH

🔗 Need help with FFmpeg? [Watch this setup video](https://youtu.be/4jAH9TmgTC0)

---

## 🔧 Installation
```bash
git clone https://github.com/Kgadiete/SpotiFetch.git
cd SpotiFetch
pip install -r requirements.txt
```

---

## 🌍 Environment Setup
Create a `.env` file in the root directory with your Spotify API credentials:
```ini
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```
Get your credentials at: https://developer.spotify.com/dashboard/

---

## 🚀 Usage
```bash
python SpotiFetch.py <spotify_playlist_url> [-o OUTPUT_DIR] [--clear-cache]
```

### ✅ Example
```bash
python SpotiFetch.py "https://open.spotify.com/playlist/1AbCxyz123..." -o "~/Music/Downloads"
```

### Options
- `-o, --output` : (Optional) Directory to save MP3 files. Default: `~/Downloads/SpotiFetch`
- `--clear-cache` : Clears download history so everything is redownloaded.

---

## 💡 Notes
- Audio is sourced from YouTube via `yt-dlp`, then converted to MP3 using `ffmpeg`
- The script auto-detects and skips existing `.mp3` files
- Supports playlists only (tracks support can be added later)

---

## 🧵 Tags
`#SpotiFetch` `#SpotifyDownloader` `#yt-dlp` `#ffmpeg` `#spotdl` `#CLItools` `#SpotifyToMP3`

## 📜 License
MIT License
