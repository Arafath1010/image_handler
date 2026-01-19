FROM python:3.9-slim

# Install system dependencies for Tkinter and image processing
RUN apt-get update && apt-get install -y \
    python3-tk \
    libtk8.6 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxss1 \
    libgomp1 \
    libglib2.0-0 \
    libsm6 \
    libxft2 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY main.py .
COPY static/ ./static/
COPY templates/ ./templates/

# Create temp directory
RUN mkdir -p temp

# Set environment variables for Tkinter
ENV DISPLAY=:0
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "main.py"]