FROM python:3.10.14-slim

WORKDIR /app

COPY . /app/

COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "object_detection.py"]
