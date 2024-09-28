import typer
from rich.console import Console
from rich.progress import Progress
from . import video_utils

console = Console()
app = typer.Typer()

@app.command()
def main(
    directory: str = typer.Option(".", help="Directory containing videos"),
    angle: int = typer.Option(90, help="Rotation angle (90, 180, or 270)"),
    preview: bool = typer.Option(False, "--preview", "-p", help="Preview rotations without applying changes"),
    output: str = typer.Option(None, "--output", "-o", help="Specify output directory for rotated videos"),
) -> None:
    """
    Run the main application to rotate batches of videos.
    """
    video_utils.check_ffmpeg()
    
    if directory == ".":
        directory = video_utils.select_directory()
    
    video_files = video_utils.get_video_files(directory)
    
    if not video_files:
        console.print("No video files found in the selected folder. Exiting.")
        raise typer.Exit(1)
    
    if preview:
        video_utils.preview_rotations(video_files, angle)
    else:
        with Progress() as progress:
            task = progress.add_task("[green]Rotating videos...", total=len(video_files))
            for video in video_files:
                video_utils.rotate_video(video, angle, output)
                progress.update(task, advance=1)
    
    console.print(f"[bold green]Rotation complete![/bold green] Processed {len(video_files)} videos.")

if __name__ == "__main__":
    app()
