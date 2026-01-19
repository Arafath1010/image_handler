# Image Handler - Docker Setup

This Docker setup allows you to run the Tkinter-based image processing application in a containerized environment.

## Prerequisites

- Docker installed on your system
- X11 display server (Linux/Mac) or X11 forwarding tools (Windows)

## Building the Docker Image

```bash
# Navigate to the project directory
cd e:\image_handler

# Build the Docker image
docker build -t image-handler .
```

## Running the Application

### On Linux:

```bash
# Allow Docker to connect to X11
xhost +local:docker

# Run the container with X11 forwarding
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $(pwd):/app \
  image-handler

# After running, revoke X11 access
xhost -local:docker
```

### On macOS:

First, install XQuartz:
```bash
brew install xquartz
```

Then run:
```bash
# Allow connections from network clients
open -a XQuartz
# In XQuartz preferences -> Security, check "Allow connections from network clients"

# Get your IP address
IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')

# Run the container
docker run -it --rm \
  -e DISPLAY=$IP:0 \
  -v $(pwd):/app \
  image-handler
```

### On Windows:

#### Option 1: Using MobaXterm (Recommended)
1. Install MobaXterm from https://mobaxterm.mobatek.net/
2. Start MobaXterm
3. Run this single-line command in MobaXterm's terminal:
```bash
docker run -it --rm -e DISPLAY=host.docker.internal:0 -v //c/image_handler:/app image-handler
```

#### Option 2: Using Windows Command Prompt
Run this single-line command in Command Prompt:
```cmd
docker run -it --rm -e DISPLAY=host.docker.internal:0 -v //c/image_handler:/app image-handler
```

**Note:** If your project is not in `C:\image_handler`, replace `//c/image_handler` with the correct path in the format `//drive_letter/path/to/project` (e.g., `//d/myproject` for `D:\myproject`).

#### Option 3: Using PowerShell
In PowerShell, you can use backticks (`) for line continuation:
```powershell
docker run -it --rm `
  -e DISPLAY=host.docker.internal:0 `
  -v //c/image_handler:/app `
  image-handler
```

#### Option 4: Using VcXsrv
1. Install VcXsrv from https://sourceforge.net/projects/vcxsrv/
2. Start VcXsrv with default settings
3. Run the same command as above in your preferred terminal

## Quick Windows Setup (Step-by-Step)

### Step 1: Install MobaXterm
1. Download from: https://mobaxterm.mobatek.net/
2. Install and start MobaXterm
3. **Important**: Keep MobaXterm running in the background

### Step 2: Run the Docker Container
In MobaXterm's terminal (not Windows Command Prompt), run:
```bash
docker run -it --rm -e DISPLAY=host.docker.internal:0 -v //e/image_handler:/app image-handler
```

### Step 3: Alternative - Windows Command Prompt
If you prefer Command Prompt, first ensure MobaXterm is running, then:
```cmd
docker run -it --rm -e DISPLAY=host.docker.internal:0 -v //e/image_handler:/app image-handler
```

## Troubleshooting

### Display Connection Errors:
- **"couldn't connect to display"**: No X11 server running
  - **Solution**: Install and start MobaXterm, VcXsrv, or X410
  - **MobaXterm**: Easiest option - includes X11 server built-in
  - **VcXsrv**: Download from https://sourceforge.net/projects/vcxsrv/
  - **X410**: Available in Microsoft Store

- **Firewall blocking**: Windows Firewall may block X11 connections
  - **Solution**: Temporarily disable firewall or add exceptions for X11 ports

- **Wrong DISPLAY variable**: 
  - **MobaXterm/VcXsrv**: Use `host.docker.internal:0`
  - **X410**: May need different DISPLAY value

### Command Format Issues:
- **Windows Command Prompt**: Use single-line commands or PowerShell with backticks
- **Path Format**: Use `//drive_letter/path` format for Windows paths (e.g., `//c/users/yourname/project`)
- **Line Continuation**: Windows CMD doesn't support `\` for line continuation like Unix shells

### Permission Issues:
- The container runs as root, so file permissions should work
- If you encounter permission issues, check your Docker Desktop settings

### Container Won't Start:
- Verify Docker is running
- Check that the image built successfully with `docker images`
- Ensure X11 is properly configured before running

## Development

To modify the application:

1. Edit files locally
2. Rebuild the image: `docker build -t image-handler .`
3. Run the updated container

## Notes

- The application uses Tkinter, which requires a display server
- All processing happens inside the container
- File dialogs will show container paths, but files are accessible via volume mounts