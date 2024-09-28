import os
import subprocess
import sys

def check_ffmpeg():
    """Check if ffmpeg is installed."""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("ffmpeg is not installed. Would you like to install it using Homebrew? (y/n)")
        if input().lower() == 'y':
            subprocess.run(['brew', 'install', 'ffmpeg'])
            print("ffmpeg installed. Please rerun the script.")
            sys.exit()
        else:
            print("ffmpeg is required to run this script. Exiting.")
            sys.exit()

def list_directories():
    """List directories in the current working directory."""
    directories = [d for d in os.listdir() if os.path.isdir(d)]
    for i, directory in enumerate(directories):
        print(f"{i + 1}: {directory}")
    return directories

def rotate_videos(video_files):
    """Rotate videos by updating their metadata for 90-degree rotation using ExifTool."""
    for video in video_files:
        input_file = os.path.abspath(video)
        
        print(f"Processing: {input_file}")

        command = [
            'exiftool',
            '-Rotation=90',  # Set rotation to 90 degrees
            '-n',  # Preserve original metadata tags
            '-overwrite_original',  # Overwrite the original file
            input_file
        ]
        
        print("Running command:", ' '.join(command))

        try:
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Successfully processed: {input_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error processing {input_file}:")
            print(e.stderr)

    print("Video rotation complete.")

if __name__ == "__main__":
    check_ffmpeg()
    
    print("Select a folder containing videos:")
    directories = list_directories()

    # Prompt the user for folder selection without subtracting 1
    folder_choice = int(input("Enter the number of the folder: "))  # No -1 here
    if folder_choice < 1 or folder_choice > len(directories):
        print("Invalid choice. Exiting.")
        sys.exit()

    # Access the selected folder correctly
    selected_folder = directories[folder_choice - 1].strip()  # Still need to strip whitespace
    print(f"Selected folder: '{selected_folder}'")  # Debug line with quotes
    print(f"Full path to selected folder: {os.path.abspath(selected_folder)}")  # Print full path
    print("Current working directory:", os.getcwd())  # Print current working directory

    # List all files in the selected folder
    all_files = os.listdir(selected_folder)
    print("All files in the selected folder:", all_files)  # Show all files

    # Check for video files
    video_files = [os.path.join(selected_folder, f) for f in all_files if f.lower().endswith(('.mp4', '.mov', '.avi'))]

    if not video_files:
        print("No video files found in the selected folder. Exiting.")
        sys.exit()

    rotate_videos(video_files)

    print(f"You selected folder number {folder_choice}: '{directories[folder_choice - 1]}'")
