# Use the latest Ubuntu image
FROM ubuntu:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip libgbm1 wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pip dependencies
RUN pip3 install --no-cache-dir getindianname==1.0.7 \
    selenium==4.15.2 \
    playwright==1.40.0

# Install Playwright browsers
RUN wget https://github.com/microsoft/playwright-python/releases/download/v1.40.0/playwright-1.40.0-linux.zip && \
    unzip playwright-1.40.0-linux.zip -d /opt/ && \
    rm playwright-1.40.0-linux.zip && \
    PLAYWRIGHT_BROWSERS_PATH=/opt/ /opt/playwright/install

# Create and set the working directory
WORKDIR /app

# Copy the Python script to the working directory
COPY script.py .

# Run the Python script
CMD ["python3", "script.py"]
