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

# All previous lines for 'useradd', 'chown', and 'USER flaskuser' have been removed.
# The container will now run as the default user, which is root (UID 0).

# Expose Flask port
EXPOSE 5000

# Run the Flask app using Gunicorn (production server)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
