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

# 1. Create non-root user with explicit UID/GID 1000 (still running as root)
RUN useradd -m -u 1000 -g 1000 flaskuser

# 2. Create DB folder and set permissions (must be run as root)
RUN mkdir -p /app/database && chown -R flaskuser:flaskuser /app

# 3. Finally, switch to the non-root user
USER flaskuser

# Expose Flask port
EXPOSE 5000

# Run the Flask app using Gunicorn (production server)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
