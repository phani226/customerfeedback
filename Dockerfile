# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

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

