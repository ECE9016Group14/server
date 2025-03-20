#
FROM python:3.10.9
#
WORKDIR /code
COPY . /code
RUN apt update
RUN apt install nano
#
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt --no-cache-dir
CMD ["bash", "-c", "python -m uvicorn src.app.main:app --host 0.0.0.0 --port 8080"]