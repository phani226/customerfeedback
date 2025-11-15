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
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the entire project
COPY . .
 
# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
 
# Expose Flask port
EXPOSE 5000
 
# Optional but recommended: run container as non-root user
RUN useradd -m flaskuser
USER flaskuser
 
# Run the Flask app
CMD ["python", "app.py"]
