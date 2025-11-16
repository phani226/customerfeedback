# Use lightweight Python image
FROM python:3.11-slim

# Install system dependencies (SQLite support)
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install gunicorn

# Copy the entire project
COPY . .

# Create DB folder and set correct permissions BEFORE switching user
RUN mkdir -p /app/database && chown -R flaskuser:flaskuser /app

# Create non-root user with explicit UID/GID 1000
# THIS IS THE CRITICAL CHANGE: Matches the fsGroup: 1000 in your Deployment
RUN useradd -m -u 1000 -g 1000 flaskuser 
USER flaskuser

# Expose Flask port
EXPOSE 5000

# Run the Flask app using Gunicorn (production server)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
