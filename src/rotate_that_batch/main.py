from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Input, Select, Static

from . import video_utils
from .logger import logger


class RotateThatBatchApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #main {
        width: 80%;
        height: auto;
        border: solid green;
        padding: 1 2;
    }

    Button {
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Welcome to Rotate That Batch!", id="title"),
            Input(placeholder="Enter path to video directory...", id="input"),
            Select([(90, "90°"), (180, "180°"), (270, "270°")], id="angle", value=90),
            Button("Preview", id="preview"),
            Button("Rotate", id="rotate"),
            Static(id="output"),
            id="main",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        directory = self.query_one("#input").value
        angle = self.query_one("#angle").value
        video_files = video_utils.get_video_files(directory)

        if not video_files:
            self.query_one("#output").update(
                "No video files found in the selected folder."
            )
            logger.warning(f"No video files found in directory: {directory}")
            return

        if event.button.id == "preview":
            logger.info(
                f"Starting preview for directory: {directory} with angle: {angle}"
            )
            video_utils.preview_rotations(video_files, angle)
            self.query_one("#output").update("Preview complete!")
        elif event.button.id == "rotate":
            logger.info(
                f"Starting rotation process for directory: {directory} with angle: {angle}"
            )
            for video in video_files:
                video_utils.rotate_video(video, angle)
            self.query_one("#output").update(f"Rotated {len(video_files)} videos.")
            logger.info(f"Rotation complete. Processed {len(video_files)} videos.")


if __name__ == "__main__":
    app = RotateThatBatchApp()
    app.run()
