import pytest
from typer.testing import CliRunner
from rotate_that_batch.cli import app
from rotate_that_batch.main import RotateThatBatchApp
from rotate_that_batch import video_utils, config
from rotate_that_batch.logger import logger
import os
import tempfile
import configparser

runner = CliRunner()

def test_main_with_directory(mocker):
    mock_check_ffmpeg = mocker.patch('rotate_that_batch.video_utils.check_ffmpeg')
    mock_get_video_files = mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=['video1.mp4', 'video2.mp4'])
    mock_rotate_video = mocker.patch('rotate_that_batch.video_utils.rotate_video')

    result = runner.invoke(app, ["--directory", "/test/dir", "--angle", "180"])
    
    assert result.exit_code == 0
    assert "Rotation complete!" in result.stdout
    mock_check_ffmpeg.assert_called_once()
    mock_get_video_files.assert_called_once_with("/test/dir")
    assert mock_rotate_video.call_count == 2

def test_main_no_videos(mocker):
    mocker.patch('rotate_that_batch.video_utils.check_ffmpeg')
    mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=[])

    result = runner.invoke(app, ["--directory", "/empty/dir"])
    
    assert result.exit_code != 0
    assert "No video files found" in result.stdout

def test_main_directory_selection(mocker):
    mock_get_video_files = mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=['video1.mp4'])
    mock_rotate_video = mocker.patch('rotate_that_batch.video_utils.rotate_video')
    mock_check_ffmpeg = mocker.patch('rotate_that_batch.video_utils.check_ffmpeg')
    
    result = runner.invoke(app, ["--directory", "dir1"])
    
    assert result.exit_code == 0
    mock_check_ffmpeg.assert_called_once()
    mock_get_video_files.assert_called_once_with('dir1')
    mock_rotate_video.assert_called()
    assert "Rotation complete!" in result.stdout

@pytest.mark.asyncio
async def test_rotate_that_batch_app(mocker):
    mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=['video1.mp4'])
    mock_rotate_video = mocker.patch('rotate_that_batch.video_utils.rotate_video')
    mock_preview_rotations = mocker.patch('rotate_that_batch.video_utils.preview_rotations')

    app = RotateThatBatchApp()
    async with app.run_test() as pilot:
        title = pilot.app.query_one("#title")
        assert title.renderable.plain == "Welcome to Rotate That Batch!"

        input_widget = pilot.app.query_one("#input")
        input_widget.value = "/test/dir"

        angle_select = pilot.app.query_one("#angle")
        angle_select.value = 180

        await pilot.click("#preview")
        mock_preview_rotations.assert_called_once()

        await pilot.click("#rotate")
        mock_rotate_video.assert_called_once()

        output = pilot.app.query_one("#output")
        assert "Rotated 1 videos" in output.renderable.plain

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

def test_rotate_video(mocker):
    mock_exiftool = mocker.patch('exiftool.ExifToolHelper')
    video_file = "/path/to/video1.mp4"
    video_utils.rotate_video(video_file, 90)
    mock_exiftool.return_value.__enter__.return_value.execute.assert_called_once()

def test_main_cli_with_directory(mocker):
    mocker.patch('rotate_that_batch.video_utils.check_ffmpeg')
    mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=["/path/to/video.mp4"])
    mock_rotate_video = mocker.patch('rotate_that_batch.video_utils.rotate_video')
    
    result = runner.invoke(app, ["--directory", "/test/dir", "--angle", "180"])
    assert result.exit_code == 0
    assert "Rotation complete!" in result.stdout
    mock_rotate_video.assert_called_once()

# New tests

def test_config_file_system(mocker):
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    mocker.patch('os.path.exists', return_value=True)
    mocker.patch('configparser.ConfigParser.read')

    # Test loading config
    loaded_config = config.load_config()
    assert isinstance(loaded_config, configparser.ConfigParser)

    # Test getting config value
    value = config.get_config_value('default_angle', '90')
    assert value == '90'

    # Test setting config value
    config.set_config_value('default_angle', '180')
    mock_open.assert_called_with(config.CONFIG_FILE, 'w')

def test_preview_functionality(mocker):
    mock_subprocess = mocker.patch('subprocess.run')
    mock_input = mocker.patch('builtins.input', return_value='')
    mock_os_remove = mocker.patch('os.remove')
    
    video_files = ['/path/to/video1.mp4', '/path/to/video2.mp4']
    video_utils.preview_rotations(video_files, 90)
    
    assert mock_subprocess.call_count == 4  # 2 calls for ffmpeg, 2 for opening preview
    assert mock_input.call_count == 2  # Once for each video file
    assert mock_os_remove.call_count == 2  # Once for each temporary file

def test_main_with_preview(mocker):
    mocker.patch('rotate_that_batch.video_utils.check_ffmpeg')
    mock_preview = mocker.patch('rotate_that_batch.video_utils.preview_rotations')
    mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=["/path/to/video.mp4"])
    
    result = runner.invoke(app, ["--directory", "/test/dir", "--angle", "180", "--preview"])
    assert result.exit_code == 0
    assert "Preview complete" in result.stdout
    mock_preview.assert_called_once()

def test_main_with_output_directory(mocker):
    mocker.patch('rotate_that_batch.video_utils.check_ffmpeg')
    mock_rotate_video = mocker.patch('rotate_that_batch.video_utils.rotate_video')
    mocker.patch('rotate_that_batch.video_utils.get_video_files', return_value=["/path/to/video.mp4"])
    
    result = runner.invoke(app, ["--directory", "/test/dir", "--angle", "180", "--output", "/output/dir"])
    assert result.exit_code == 0
    assert "Rotation complete" in result.stdout
    mock_rotate_video.assert_called_once_with("/path/to/video.mp4", 180, "/output/dir")

def test_main_with_invalid_angle(mocker):
    result = runner.invoke(app, ["--directory", "/test/dir", "--angle", "45"])
    assert result.exit_code != 0
    assert "Invalid angle" in result.stdout

def test_check_ffmpeg_not_installed(mocker):
    mocker.patch('subprocess.run', side_effect=FileNotFoundError)
    mock_exit = mocker.patch('sys.exit')
    mock_input = mocker.Mock(return_value='n')
    
    video_utils.check_ffmpeg(install_prompt=mock_input)
    
    mock_input.assert_called_once()
    mock_exit.assert_called_once_with(1)