# Run these commands in the GitHub Codespace terminal (from the repository root)

# 1. Create a Docker network so the two containers can talk to each other by name
docker network create superkart-net

# 2. Build and run the Flask backend (port 7860)
docker build -t superkart-backend ./backend_files
docker run -d --name superkart-backend --network superkart-net -p 7860:7860 superkart-backend

# 3. Build and run the Streamlit frontend (port 8501)
docker build -t superkart-frontend ./frontend_files
docker run -d --name superkart-frontend --network superkart-net -p 8501:8501 \
    -e BACKEND_URL=http://superkart-backend:7860 superkart-frontend

# 4. Check both containers are up
docker ps
