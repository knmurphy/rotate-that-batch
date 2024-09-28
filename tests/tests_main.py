import pytest
from typer.testing import CliRunner
from rotate_that_batch.main import app
from rotate_that_batch import video_utils
import os
import tempfile

runner = CliRunner()

def test_main_with_directory(mocker):
    mock_check_ffmpeg = mocker.patch('rotate_that_batch.video_utils.check_ffmpeg')
    mock_get_video_files = mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=['video1.mp4', 'video2.mp4'])
    mock_rotate_videos = mocker.patch('rotate_that_batch.video_utils.rotate_videos')

    result = runner.invoke(app, ["--directory", "/test/dir", "--angle", "180"])
    
    assert result.exit_code == 0
    assert "Rotation complete!" in result.stdout
    assert "Processed 2 videos" in result.stdout
    mock_check_ffmpeg.assert_called_once()
    mock_get_video_files.assert_called_once_with("/test/dir")
    assert mock_rotate_videos.call_count == 2

def test_main_no_videos(mocker):
    mocker.patch('rotate_that_batch.video_utils.check_ffmpeg')
    mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=[])

    result = runner.invoke(app, ["--directory", "/empty/dir"])
    
    assert result.exit_code == 1
    assert "No video files found" in result.stdout

def test_main_directory_selection(mocker):
    mock_list_directories = mocker.patch('rotate_that_batch.video_utils.list_directories', return_value=['dir1', 'dir2'])
    mock_get_video_files = mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=['video1.mp4'])
    mock_rotate_videos = mocker.patch('rotate_that_batch.video_utils.rotate_videos')
    mocker.patch('typer.prompt', return_value="1")

    result = runner.invoke(app)
    
    assert result.exit_code == 0
    mock_list_directories.assert_called_once()
    mock_get_video_files.assert_called_once_with('dir1')
    mock_rotate_videos.assert_called_once()

@pytest.mark.asyncio
async def test_rotate_that_batch_app():
    from rotate_that_batch.main import RotateThatBatchApp
    app = RotateThatBatchApp()
    async with app.run_test() as pilot:
        title = pilot.app.query_one("#title")
        assert title.render() == "Welcome to Rotate That Batch!"

        input_widget = pilot.app.query_one("#input")
        await input_widget.press_keys("/test/dir")
        
        mock_get_video_files = pilot.app.patch('rotate_that_batch.video_utils.get_video_files', return_value=['video1.mp4'])
        mock_rotate_videos = pilot.app.patch('rotate_that_batch.video_utils.rotate_videos')

        await pilot.click("#submit")
        
        output = pilot.app.query_one("#output")
        assert output.render() == "Rotated 1 videos."
        mock_get_video_files.assert_called_once_with("/test/dir")
        mock_rotate_videos.assert_called_once()

def test_list_directories():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.mkdir(os.path.join(tmpdir, "test_dir"))
        os.chdir(tmpdir)
        dirs = video_utils.list_directories()
        assert "test_dir" in dirs

def test_get_video_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        open(os.path.join(tmpdir, "test.mp4"), "w").close()
        open(os.path.join(tmpdir, "test.txt"), "w").close()
        videos = video_utils.get_video_files(tmpdir)
        assert len(videos) == 1
        assert videos[0].endswith("test.mp4")

def test_rotate_videos(mocker):
    mock_exiftool = mocker.patch('exiftool.ExifToolHelper')
    video_files = ["/path/to/video1.mp4", "/path/to/video2.mp4"]
    video_utils.rotate_videos(video_files, 90)
    assert mock_exiftool.return_value.__enter__.return_value.execute.call_count == 2

def test_main_cli_with_directory(mocker):
    mocker.patch('rotate_that_batch.video_utils.check_ffmpeg')
    mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=["/path/to/video.mp4"])
    mocker.patch('rotate_that_batch.video_utils.rotate_videos')
    
    result = runner.invoke(app, ["--directory", "/test/dir", "--angle", "180"])
    assert result.exit_code == 0
    assert "Rotation complete!" in result.stdout
