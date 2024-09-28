import typer
from rich.console import Console
from rich.progress import Progress
from . import video_utils
from .config import get_config_value, set_config_value
from .logger import logger

console = Console()
app = typer.Typer()


@app.command()
def main(
    directory: str = typer.Option(
        get_config_value("default_directory", "."), help="Directory containing videos"
    ),
    angle: int = typer.Option(
        int(get_config_value("default_angle", 90)),
        help="Rotation angle (90, 180, or 270)",
    ),
    preview: bool = typer.Option(
        False, help="Preview rotations without applying changes"
    ),
    output: str = typer.Option(
        get_config_value("output_directory"), help="Output directory for rotated videos"
    ),
):
    logger.info(f"Starting rotation process for directory: {directory}")
    video_utils.check_ffmpeg()

    if angle not in [90, 180, 270]:
        logger.error(f"Invalid angle: {angle}")
        console.print("[bold red]Invalid angle. Please use 90, 180, or 270.[/bold red]")
        raise typer.Exit(code=1)

    video_files = video_utils.get_video_files(directory)

    if not video_files:
        logger.warning(f"No video files found in directory: {directory}")
        console.print("No video files found in the selected folder. Exiting.")
        raise typer.Exit(code=1)

    if preview:
        video_utils.preview_rotations(video_files, angle)
        console.print("Preview complete!")
    else:
        with Progress() as progress:
            task = progress.add_task(
                "[green]Rotating videos...", total=len(video_files)
            )
            for video in video_files:
                video_utils.rotate_video(video, angle, output)
                progress.update(task, advance=1)

        logger.info(f"Rotation complete. Processed {len(video_files)} videos.")
        console.print(
            f"[bold green]Rotation complete![/bold green] Processed {len(video_files)} videos."
        )

    # Save the used values to config
    set_config_value("default_directory", directory)
    set_config_value("default_angle", angle)
    if output:
        set_config_value("output_directory", output)


if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {str(e)}")
        console.print(f"[bold red]An unexpected error occurred: {str(e)}[/bold red]")
        raise typer.Exit(code=1)
