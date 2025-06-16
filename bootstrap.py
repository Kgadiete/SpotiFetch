import subprocess
import sys
import os

def install_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to install required packages.")
        sys.exit(1)

def check_and_install():
    try:
        import yt_dlp
        import aiohttp
        import requests
        from dotenv import load_dotenv
    except ImportError:
        print("[!] Missing dependencies required to run this program.")
        choice = input("Do you want to install them now? [Y/n]: ").strip().lower()
        if choice in ('', 'y', 'yes'):
            install_requirements()
            print("[INFO] Dependencies installed. Please re-run the script.")
        else:
            print("[INFO] Exiting without installing dependencies.")
        sys.exit(0)
