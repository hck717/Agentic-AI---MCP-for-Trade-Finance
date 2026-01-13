FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set PYTHONPATH to include the root directory
ENV PYTHONPATH=/app

# Expose Streamlit port
EXPOSE 8501

# Default command to run the Streamlit App
CMD ["streamlit", "run", "app/ui/streamlit_app.py", "--server.address=0.0.0.0"]
