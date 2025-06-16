#!/usr/bin/env python3
from bootstrap import check_and_install
check_and_install()

import os
import sys
import json
import base64
import hashlib
import asyncio
import signal
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
import yt_dlp
import requests
import argparse
from dotenv import load_dotenv

# Load environment
load_dotenv()

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"
CACHE_FILE = "downloaded_tracks.json"
DEFAULT_OUTPUT = Path.home() / "Downloads" / "SpotiFetch"

# ANSI codes
GREEN = "\033[92m"
RESET = "\033[0m"

# Global shutdown flag
global_shutdown = False

def handle_sigint(sig, frame):
    global global_shutdown
    print("\n[INFO] Received interrupt, exiting...")
    global_shutdown = True

signal.signal(signal.SIGINT, handle_sigint)

class Downloader:
    def __init__(self, output_dir: Path, token: str, cache: dict):
        self.output = output_dir
        self.token = token
        self.cache = cache
        self.session = None
        self.ffmpeg = None

    @staticmethod
    def find_ffmpeg() -> str:
        path = shutil.which("ffmpeg")
        if not path:
            print("[ERROR] FFmpeg not found. Install and add to PATH.")
            sys.exit(1)
        return path

    async def setup(self):
        self.session = aiohttp.ClientSession()
        self.ffmpeg = self.find_ffmpeg()

    async def fetch_playlist(self, playlist_id: str):
        url = f"{SPOTIFY_API_BASE}/playlists/{playlist_id}/tracks"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"limit": 50}
        tracks = []
        while url and not global_shutdown:
            async with self.session.get(url, headers=headers, params=params) as r:
                if r.status != 200:
                    print(f"[ERROR] Spotify API error: {r.status}")
                    break
                data = await r.json()
            for item in data.get("items", []):
                t = item.get("track")
                if t:
                    tracks.append((t["name"], t["artists"][0]["name"]))
            url = data.get("next")
            params = None
        return tracks

    async def download_and_convert(self, name: str, artist: str, idx: int, total: int):
        if global_shutdown:
            return
        safe_name = name.replace('/', '_')
        safe_artist = artist.replace('/', '_')
        mp3_file = self.output / f"{safe_artist} - {safe_name}.mp3"

        if mp3_file.exists():
            print(f"{GREEN}[{idx}/{total}] Exists:{RESET} {mp3_file.name}")
            return

        # Download via yt-dlp
        temp = str(self.output / f"{safe_artist} - {safe_name}.%(ext)s")
        opts = {"format": "bestaudio/best", "outtmpl": temp, "quiet": True}
        ydl = yt_dlp.YoutubeDL(opts)
        query = f"ytsearch:{name} {artist} audio"
        try:
            info = await asyncio.get_event_loop().run_in_executor(None, ydl.extract_info, query, True)
        except Exception as e:
            print(f"[{idx}/{total}] Download failed: {e}")
            return
        if not info:
            print(f"[{idx}/{total}] Download returned no info")
            return
        if "entries" in info:
            info = info["entries"][0]
        ext = info.get("ext", "m4a")
        src = self.output / f"{safe_artist} - {safe_name}.{ext}"

        # Convert
        cmd = [self.ffmpeg, '-y', '-i', str(src), '-vn', '-codec:a', 'libmp3lame', '-b:a', '192k', '-ar', '44100', str(mp3_file)]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"[{idx}/{total}] Conversion failed: {e}")
            return

        try:
            src.unlink()
        except:
            pass

        print(f"{GREEN}[{idx}/{total}] Completed:{RESET} {mp3_file.name}")

    async def run(self, playlist_id: str):
        await self.setup()
        tracks = await self.fetch_playlist(playlist_id)
        total = len(tracks)
        self.output.mkdir(parents=True, exist_ok=True)

        for i, (name, artist) in enumerate(tracks, 1):
            if global_shutdown:
                break
            await self.download_and_convert(name, artist, i, total)

        await self.session.close()

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="Spotify playlist URL")
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPUT, type=Path)
    parser.add_argument('--clear-cache', action='store_true')
    args = parser.parse_args()

    if args.clear_cache:
        print("[INFO] Cache cleared")
        cache = {}
    else:
        cache = json.load(open(CACHE_FILE)) if os.path.exists(CACHE_FILE) else {}

    cid = os.getenv('SPOTIFY_CLIENT_ID')
    secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    auth = base64.b64encode(f"{cid}:{secret}".encode()).decode()
    r = requests.post(SPOTIFY_TOKEN_URL, headers={'Authorization': f'Basic {auth}'}, data={'grant_type': 'client_credentials'})
    if r.status_code != 200:
        print(f"[ERROR] Token fetch failed: {r.status_code}")
        sys.exit(1)
    token = r.json().get('access_token')

    parts = urlparse(args.url).path.split('/')
    if 'playlist' not in parts:
        print("[ERROR] Invalid URL: Please provide a playlist URL")
        sys.exit(1)
    pid = parts[parts.index('playlist') + 1].split('?')[0]

    downloader = Downloader(args.output, token, cache)
    await downloader.run(pid)

    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

    print("[INFO] All done!")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[INFO] Interrupted by user. Exiting.")
