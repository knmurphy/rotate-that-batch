from typing import List, Tuple
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Button, DirectoryTree, Footer, Header, Static
from textual.containers import Container, Horizontal
from .video_utils import rotate_video, get_video_files

class RotateThatBatch(App):
    CSS_PATH = "rotate_that_batch.css"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Horizontal(
                DirectoryTree(".", id="input_dir"),
                DirectoryTree(".", id="output_dir"),
            ),
            Static("Select input and output directories", id="status_text"),
            Button("Rotate Videos", id="rotate_button"),
        )
        yield Footer()

    rotation_options: List[Tuple[str, object]] = [("90", 90), ("180", 180), ("270", 270)]

    def on_mount(self) -> None:
        self.input_dir = self.query_one("#input_dir", DirectoryTree)
        self.output_dir = self.query_one("#output_dir", DirectoryTree)
        self.status_text = self.query_one("#status_text", Static)

    def on_button_pressed(self) -> None:
        input_dir = Path(self.input_dir.path if hasattr(self.input_dir, 'path') else str(self.input_dir))
        output_dir = Path(self.output_dir.path if hasattr(self.output_dir, 'path') else str(self.output_dir))
        
        self.update_status(f"Processing videos in {input_dir}")
        
        video_files = get_video_files(str(input_dir))
        for video_file in video_files:
            rotate_video(video_file, 90, str(output_dir))
        
        self.update_status(f"Videos processed. Output directory: {output_dir}")
        self.update_status("Done!")

    def update_status(self, message: str) -> None:
        self.status_text.update(message)

if __name__ == "__main__":
    app = RotateThatBatch()
    app.run()
