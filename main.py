# A Wrapper around yt-dlp that downloads audio in mp3 format from yt videos and embeds the thumbnail, artist etc. too

import re
import subprocess
import sys

from rich.console import Console
from rich.panel import Panel
from rich import print

import questionary


def download_audio(url: str, embed_thumbnail=True, add_metadata=True, destination_path: str=None):
    '''
    Download the audio from a youtube video and embed the metadata of it
    
    cmd: yt-dlp -x --audio-format mp3 --audio-quality 0 --embed-thumbnail --add-metadata <url>    
    
    :param url: Youtube Video URL
    :type url: str
    '''
    
    # Setup the yt-dlp command
    
    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "-x",               # Audio only
        "--audio-format",   # Audio format
        "mp3",              # .mp3
        "--audio-quality",  # Audio Quality
        "0",                # Best possible quality
        url
    ]
    
    optional_flags = [
        "--embed-thumbnail" if embed_thumbnail else None,
        "--add-metadata" if add_metadata else None,
        "-P" if destination_path else None,
        destination_path if destination_path else None
    ]
    
    cmd.extend(filter(None, optional_flags))
    
    # Run the command
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
            )
        
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            "[X] Process returned non-zero exit code!\n"
            f"Exit code: {e.returncode}\n"
            f"Command: {' '.join(map(str, e.cmd))}\n\n"
            f"STDERR:\n{(e.stderr or '').strip()}\n\n"
            f"STDOUT:\n{(e.stdout or '').strip()}\n"
        )
    except Exception as e:
        raise RuntimeError(f"[X] Unexpected Error:\n{e}")

def download_video(url: str, specific_quality: int = None, video_format: str = "webm"):
    """
    Download the video from a youtube video
    
    cmd: yt-dlp <url> -f <format_string>
    
    :param url: Description
    :type url: str
    """
    
    # Setup the command
    
    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        url
    ]
    print(specific_quality)
    
    audio_format = "opus" if video_format == "webm" else "m4a"
    
    fmt = (
        f"bv*[ext={video_format}]"
        + (f"[height<={specific_quality}]" if specific_quality is not None else "")
        + f"+ba[ext={audio_format}]/b[ext={video_format}]/b"
    )
    
    optional_flags = [
        "-f",
        fmt,
        "--merge-output-format",
        video_format
    ]
    
    cmd += optional_flags
    
    # Run the command
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
            )
        
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            "[X] Process returned non-zero exit code!\n"
            f"Exit code: {e.returncode}\n"
            f"Command: {' '.join(map(str, e.cmd))}\n\n"
            f"STDERR:\n{(e.stderr or '').strip()}\n\n"
            f"STDOUT:\n{(e.stdout or '').strip()}\n"
        )
    except Exception as e:
        raise RuntimeError(f"[X] Error:\n{e}")

def check_dependencies():
    """
    Check the required dependencies required for the script to work:
    - yt-dlp
    - ffmpeg
    """
    
    # Check if yt-dlp is installed
    
    try:
        result = subprocess.run([sys.executable, "-m", "yt_dlp", "--version"], capture_output=True, text=True, check=True)
        print("[+] yt-dlp Installed!")
    except subprocess.CalledProcessError as e:
        print(f"[X] yt-dlp Not installed!\nRun: pip install -U yt-dlp")
        sys.exit(1)
    
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
        print("[+] ffmpeg installed!")
    except FileNotFoundError as e:
        print("[X] ffmpeg not installed!\nRun: sudo apt install ffmpeg")
        sys.exit(1)

URL_RE = re.compile(r"^https?://", re.I)

def ask_url() -> str:
    return questionary.text(
        "Paste URL:",
        validate=lambda s: True if URL_RE.match(s.strip()) else "Must start with http:// or https://",
    ).ask().strip()

def main():
    """
    A python wrapper of yt-dlp that makes downloading videos and audios easy!
    """
    
    
    console = Console()
    print(Panel("Welcome to py-dlp 🎉", style="green"))

    while True:
        choice = questionary.select(
            "What's your task: ",
            choices=[
                "🎥 Download Video",
                "🔉 Download Audio",
            ]
        ).ask()
        
        if choice.startswith("🎥"):
            check_dependencies()
            
            url = ask_url()
            
            fmt = questionary.select("Format (default: .webm):", choices=["webm", "mp4"], default="webm").ask()
            q_cap = questionary.select("Quality (default: best):", choices=["best", "1080", "720", "480", "360"], default=None).ask()
            
            q = None if q_cap == "best" else int(q_cap)
            
            result = download_video(url=url, video_format=fmt, specific_quality=q)
        elif choice.startswith("🔉"):
            check_dependencies()
            
            url = ask_url()
            
            path = questionary.text("Destination Folder (default: Current):").ask()
            thumbnail_check = questionary.select(
                "Embed thumbnail to audio file:",
                choices=[
                    questionary.Choice("Yes", value=True),
                    questionary.Choice("No", value=False)
                ]
            ).ask()
            
            metadata_check = questionary.select(
                "Embed metadata to audio file:",
                choices=[
                    questionary.Choice("Yes", value=True),
                    questionary.Choice("No", value=False)
                ]
            ).ask()
            
            with console.status("Downloading...", spinner="arc"):
                result = download_audio(url=url, embed_thumbnail=thumbnail_check, add_metadata=metadata_check, destination_path=path)
            print("[+] Download Complete!")

if __name__ == "__main__":
    main()