# Rotate That Batch

When your videos are sideways, it's time to "Rotate That Batch."

## Description

Rotate That Batch is a powerful and user-friendly command-line tool designed to help you quickly rotate multiple video files. Whether you've accidentally filmed videos in the wrong orientation or received a batch of sideways videos, this tool streamlines the process of correcting their rotation.

## Features

- Batch processing: Rotate multiple videos at once
- Support for various video formats (e.g., MP4, AVI, MOV)
- Customizable rotation angles (90, 180, 270 degrees)
- Preserves original video quality
- Simple command-line interface
- Progress bar for tracking batch operations
- Option to preview rotations before applying

## Installation

### Using Homebrew

You can easily install Rotate That Batch using Homebrew:

```bash
brew install rotate-that-batch
```

### From Source

1. Clone the repository:

```bash
   git clone https://github.com/knmurphy/rotate-that-batch.git
   cd rotate-that-batch
   ```

2. Install dependencies:

```bash
   poetry install
   ```

3. Run the application:

```bash
   poetry run rotate-that-batch
   ```

## Usage

Basic usage:

```bash
rotate-that-batch /path/to/video/directory
```

Options:

- `-a, --angle`: Specify rotation angle (90, 180, or 270 degrees). Default is 90.
- `-p, --preview`: Preview rotations without applying changes.
- `-o, --output`: Specify output directory for rotated videos.

Example:

```bash
rotate-that-batch /path/to/videos -a 180 -o /path/to/output
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact

Kevin N. Murphy <https://kevinnmurphy.com/#contact>

Project Link: [https://github.com/knmurphy/rotate-that-batch](https://github.com/knmurphy/rotate-that-batch)

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [FFmpeg](https://ffmpeg.org/) for video processing capabilities
- [Poetry](https://python-poetry.org/) for dependency management
- [Typer](https://typer.tiangolo.com/) for building the CLI
- [Rich](https://rich.readthedocs.io/) for beautiful terminal formatting
