# Use the official Python 3.10.9 image
FROM python:3.10.9

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install requirements
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application
COPY . .

# Default port (can be overridden by PORT env var)
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Use shell form to properly expand $PORT
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
