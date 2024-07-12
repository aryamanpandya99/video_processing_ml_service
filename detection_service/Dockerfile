FROM python:3.10.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6

COPY . /app/

COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "object_detection.py"]
