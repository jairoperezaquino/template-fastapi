docker rm --force template-fastapi-container
docker build -t template-fastapi .
docker run -it --name template-fastapi-container -p 8000:8080 template-fastapi