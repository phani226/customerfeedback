# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential \
    && rm -rf /var/lib/apt/lists/*
    
# Copy files
COPY requirements.txt requirements.txt

# Dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the Flask port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]

