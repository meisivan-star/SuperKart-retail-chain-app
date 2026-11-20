# Python base image matching the Colab version used for training
FROM python:3.13-slim

# Working directory inside the container
WORKDIR /app

# Install dependencies first to take advantage of Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code and the serialized model
COPY . .

# Flask API listens on port 7860
EXPOSE 7860

# Serve the Flask app (object `superkart_api` in app.py) with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
