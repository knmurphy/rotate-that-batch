import typer
from rich.console import Console
from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Static
from textual.containers import Container

console = Console()
app = typer.Typer()

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
            Input(placeholder="Enter batch to rotate...", id="input"),
            Button("Rotate", id="submit"),
            Static(id="output"),
            id="main"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            input_value = self.query_one("#input").value
            result = f"Rotated batch: {input_value[::-1]}"  # Simple reverse for demonstration
            self.query_one("#output").update(result)

@app.command()
def main(batch: str = typer.Option("", help="Batch to rotate")):
    """
    Run the main application to rotate batches.
    """
    if batch:
        console.print(f"Rotated batch: [bold green]{batch[::-1]}[/bold green]")
    else:
        RotateThatBatchApp().run()

if __name__ == "__main__":
    app()
