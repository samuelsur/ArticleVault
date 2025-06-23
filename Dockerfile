FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    wget gnupg ca-certificates fonts-liberation \
    libx11-xcb1 libxcb1 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libgtk-3-0 libxss1 libasound2 libnss3 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 \
    libpangocairo-1.0-0 libcairo-gobject2 libgdk-pixbuf2.0-0 \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the application
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -s /bin/bash -m appuser

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Make sure the non-root user owns the application files
RUN chown -R appuser:appuser /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Switch to non-root user
USER appuser

# Install Playwright browsers as the non-root user
RUN playwright install chromium

# Command to run the application
CMD ["streamlit", "run", "app.py"]