# server

Use Python 3.12
Access the endpoint to see the auto-generated documentation
http://127.0.0.1:8000/docs# sm_server
# Docker
- docker build -t sm_server:latest  .
- docker tag sm_server:latest xx/sm_server:latest
- docker push xx/sm_server:latest

- docker pull xx/sm_server:latest
- docker run -itd -p 8000:8000 --env ENV=dev --name sm_server xx/sm_server:latest
- 
