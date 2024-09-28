import typer
from rich.console import Console
from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Static
from textual.containers import Container

console = Console()
app = typer.Typer()

class YourApp(App):
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
            Static("Welcome to Your Project!", id="title"),
            Input(placeholder="Enter something...", id="input"),
            Button("Submit", id="submit"),
            Static(id="output"),
            id="main"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            input_value = self.query_one("#input").value
            result = f"You entered: {input_value}"
            self.query_one("#output").update(result)

@app.command()
def main(name: str = typer.Option("World", help="Name to greet")):
    """
    Run the main application.
    """
    console.print(f"Hello, [bold green]{name}[/bold green]!")
    YourApp().run()

if __name__ == "__main__":
    app()
