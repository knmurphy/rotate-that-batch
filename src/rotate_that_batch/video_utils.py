import os
import subprocess
import sys
from typing import List, Optional
import exiftool
import typer

def check_ffmpeg() -> None:
    """Check if ffmpeg is installed."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        print("ffmpeg is not installed. Would you like to install it using Homebrew? (y/n)")
        if input().lower() == 'y':
            subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
            print("ffmpeg installed. Please rerun the script.")
            sys.exit()
        else:
            print("ffmpeg is required to run this script. Exiting.")
            sys.exit(1)

def list_directories() -> List[str]:
    """List directories in the current working directory."""
    return [d for d in os.listdir() if os.path.isdir(d)]

def select_directory() -> str:
    """Prompt user to select a directory."""
    print("Select a folder containing videos:")
    directories = list_directories()
    for i, d in enumerate(directories, 1):
        print(f"{i}: {d}")
    folder_choice = int(typer.prompt("Enter the number of the folder")) - 1
    return directories[folder_choice]

def get_video_files(directory: str) -> List[str]:
    """Get all video files in the specified directory."""
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv')
    return [os.path.join(directory, f) for f in os.listdir(directory) 
            if f.lower().endswith(video_extensions)]

def rotate_video(video: str, angle: int, output_dir: Optional[str] = None) -> None:
    """Rotate a single video by updating its metadata for rotation using ExifTool."""
    with exiftool.ExifToolHelper() as et:
        try:
            output_path = os.path.join(output_dir, os.path.basename(video)) if output_dir else video
            et.execute(f"-Rotation={angle}", "-n", "-o", output_path, video)
            print(f"Successfully processed: {video}")
        except Exception as e:
            print(f"Error processing {video}:")
            print(str(e))

def preview_rotations(video_files: List[str], angle: int) -> None:
    """Preview rotations without applying changes."""
    for video in video_files:
        # This is a placeholder. In a real implementation, you'd generate
        # a preview (e.g., a thumbnail or short clip) of the rotated video.
        print(f"Preview of {video} rotated by {angle} degrees")
