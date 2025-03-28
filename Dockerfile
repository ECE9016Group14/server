FROM python:3.10.9
#
ENV PYTHONPATH "${PYTHONPATH}:/code/src"
ENV TZ=America/Toronto
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo '$TZ' > /etc/timezone
#
WORKDIR /code
COPY requirements.txt /code
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt --no-cache-dir
#
COPY . /code
EXPOSE 8000
# CMD ["bash", "-c", "python -m uvicorn src.app.main:app --host 0.0.0.0 --port 8000"]
# CMD ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]