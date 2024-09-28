from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Static
from textual.containers import Container
from . import video_utils

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
            Button("Rotate", id="submit"),
            Static(id="output"),
            id="main"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            directory = self.query_one("#input").value
            video_files = video_utils.get_video_files(directory)
            if not video_files:
                self.query_one("#output").update("No video files found in the selected folder.")
            else:
                for video in video_files:
                    video_utils.rotate_video(video, 90)  # Default to 90 degrees
                self.query_one("#output").update(f"Rotated {len(video_files)} videos.")

if __name__ == "__main__":
    app = RotateThatBatchApp()
    app.run()
