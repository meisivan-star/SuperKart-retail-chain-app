FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit UI listens on port 8501
EXPOSE 8501

# Backend URL inside the Docker network (can be overridden with -e BACKEND_URL=...)
ENV BACKEND_URL=http://superkart-backend:7860

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", \
     "--server.enableXsrfProtection=false", "--server.enableCORS=false"]
