import pytest
from typer.testing import CliRunner
from rotate_that_batch.main import app

runner = CliRunner()

def test_main():
    result = runner.invoke(app, ["--batch", "Test"])
    assert result.exit_code == 0
    assert "Rotated batch: tseT" in result.stdout

def test_main_default():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Welcome to Rotate That Batch!" in result.stdout

@pytest.mark.asyncio
async def test_rotate_that_batch_app():
    from rotate_that_batch.main import RotateThatBatchApp
    app = RotateThatBatchApp()
    async with app.run_test() as pilot:
        title = pilot.app.query_one("#title")
        assert title.render() == "Welcome to Rotate That Batch!"

        await pilot.click("#submit")
        output = pilot.app.query_one("#output")
        assert output.render() == "Rotated batch: "

        input_widget = pilot.app.query_one("#input")
        await input_widget.press_keys("Test Batch")
        await pilot.click("#submit")
        output = pilot.app.query_one("#output")
        assert output.render() == "Rotated batch: hctaB tseT"
