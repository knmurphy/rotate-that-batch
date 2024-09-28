from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widget import Widget
from textual.widgets import Button, Input, Select, Static


class RotateThatBatchApp(App):
    CSS_PATH = "rotate_that_batch.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Static("Welcome to Rotate That Batch!", id="title")
        yield Container(
            Horizontal(
                Input(placeholder="Enter input directory", id="input"),
                Input(placeholder="Enter output directory", id="output"),
            ),
            Select(((str(angle), angle) for angle in [90, 180, 270]), id="angle"),
            Static(id="status_text"),
            Button("Preview", id="preview"),
            Button("Rotate", id="rotate"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "preview":
            self.preview_rotation()
        elif event.button.id == "rotate":
            self.rotate_videos()

    def preview_rotation(self) -> None:
        status_text = self.query_one("#status_text", Static)
        status_text.update("Previewing rotation...")

    def rotate_videos(self) -> None:
        status_text = self.query_one("#status_text", Static)
        status_text.update("Rotating videos...")


if __name__ == "__main__":
    app = RotateThatBatchApp()
    app.run()
