# Image Handler

A desktop application for batch processing images with a modern Tkinter GUI.

## Features

- Change image DPI
- Convert image formats (JPG, JPEG, TIF, WEBP, PNG)
- Resize images by dimensions, aspect ratio, percentage, or total pixels
- Batch processing with folder-based input/output
- Real-time processing logs with color-coded messages
- Results dashboard showing success/failure status
- Modern GUI with intuitive controls

## Installation

### Local Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

### Docker Installation

See [DOCKER_README.md](DOCKER_README.md) for complete Docker setup instructions.

#### Quick Docker Start:

```bash
# Build the image
docker build -t image-handler .

# Run on Linux/Mac
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $(pwd):/app image-handler

# Run on Windows (with MobaXterm)
docker run -it --rm -e DISPLAY=host.docker.internal:0 -v //c/image_handler:/app image-handler
```

## Usage

1. **Select Input Folder**: Click "Browse" to choose the folder containing images to process.

2. **Select Output Folder**: Click "Browse" to choose where processed images will be saved.

3. **Configure Processing Options**:
   - **Format**: Choose output format (JPG, PNG, TIF, WEBP, etc.)
   - **DPI**: Set the DPI for the output images
   - **Width/Height**: Set specific dimensions in pixels
   - **Resize %**: Scale images by percentage
   - **Aspect Ratio**: Maintain aspect ratio (e.g., 16:9)

4. **Process Images**: Click "Process Images" to start batch processing.

5. **Monitor Progress**: Watch the real-time logs on the right side and view results in the table.

6. **Review Results**: The results table shows filename, original size, new size, changes made, and status.

## Interface Layout

- **Left Panel**: Input/output controls, processing options, and results table
- **Right Panel**: Real-time processing logs with color-coded message types

## Supported Formats

- Input: JPG, JPEG, PNG, TIF, TIFF, WEBP, BMP, and other PIL-supported formats
- Output: JPG, JPEG, PNG, TIF, WEBP

## Notes

- The application automatically creates the output folder if it doesn't exist
- Processing is done in the background to prevent UI freezing
- All operations are logged with timestamps and color coding
- Failed operations are clearly marked in the results table