import os
import subprocess
import sys
from typing import List, Optional
import exiftool
from .logger import logger


def check_ffmpeg(install_prompt=input):
    """Check if ffmpeg is installed."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        logger.info("ffmpeg is installed and working correctly.")
    except FileNotFoundError:
        logger.warning("ffmpeg is not installed.")
        print(
            "ffmpeg is not installed. Would you like to install it using Homebrew? (y/n)"
        )
        if install_prompt().lower() == "y":
            try:
                subprocess.run(["brew", "install", "ffmpeg"], check=True)
                logger.info("ffmpeg installed successfully.")
                print("ffmpeg installed. Please rerun the script.")
            except subprocess.CalledProcessError:
                logger.error("Failed to install ffmpeg using Homebrew.")
                print("Failed to install ffmpeg. Please install it manually.")
            sys.exit()
        else:
            logger.info("User chose not to install ffmpeg. Exiting.")
            print("ffmpeg is required to run this script. Exiting.")
            sys.exit(1)


def list_directories() -> List[str]:
    """List all directories in the current working directory."""
    directories = [d for d in os.listdir() if os.path.isdir(d)]
    logger.info(
        f"Found {len(directories)} directories in the current working directory."
    )
    return directories


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
    video_extensions = (".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv")
    video_files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(video_extensions)
    ]
    logger.info(f"Found {len(video_files)} video files in directory: {directory}")
    return video_files


def rotate_video(video_file: str, angle: int, output_dir: str = None) -> None:
    """Rotate a video file by the specified angle."""
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, os.path.basename(video_file))
    else:
        output_file = video_file

    try:
        with exiftool.ExifToolHelper() as et:
            et.execute(f"-Rotation={angle}", "-overwrite_original", video_file)
        logger.info(f"Successfully rotated video: {video_file} by {angle} degrees.")
    except Exception as e:
        logger.error(f"Failed to rotate video: {video_file}. Error: {str(e)}")
        raise


def preview_rotations(video_files: List[str], angle: int) -> None:
    """Preview rotations for a list of video files."""
    logger.info(f"Previewing rotation of {len(video_files)} videos by {angle} degrees.")
    for video_file in video_files:
        try:
            # Generate a temporary rotated frame for preview
            temp_frame = f"{os.path.splitext(video_file)[0]}_preview.jpg"
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    video_file,
                    "-vf",
                    f"rotate={angle}*PI/180",
                    "-frames:v",
                    "1",
                    temp_frame,
                ],
                check=True,
                capture_output=True,
            )

            # Display the preview (this will depend on your system, adjust as needed)
            # For example, on macOS:
            subprocess.run(["open", temp_frame], check=True)

            logger.info(f"Generated preview for: {video_file}")
            input("Press Enter to continue to the next video...")

            # Clean up the temporary file
            os.remove(temp_frame)
        except subprocess.CalledProcessError as e:
            logger.error(
                f"Failed to generate preview for {video_file}. Error: {e.stderr.decode()}"
            )
        except Exception as e:
            logger.error(f"An error occurred while previewing {video_file}: {str(e)}")

    logger.info("Preview complete.")
