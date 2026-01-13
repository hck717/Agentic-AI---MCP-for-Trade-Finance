FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set PYTHONPATH to include the root directory
ENV PYTHONPATH=/app

# Default command to run the POC
CMD ["python", "-m", "app.main"]
