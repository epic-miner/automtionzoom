# Use the latest Ubuntu image
FROM ubuntu:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-venv libgbm1 wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /venv

# Upgrade pip in the virtual environment
RUN /venv/bin/pip install --upgrade pip

# Install pip dependencies within the virtual environment
RUN /venv/bin/pip install getindianname==1.0.7 \
    selenium==4.15.2 \
    playwright==1.40.0

# Install Playwright browsers
RUN /venv/bin/playwright install

# Create and set the working directory
WORKDIR /app

# Copy the Python script to the working directory
COPY script.py .

# Ensure the script uses the virtual environment's python
ENV PATH="/venv/bin:$PATH"

# Run the Python script using the virtual environment's Python
CMD ["python", "script.py"]
