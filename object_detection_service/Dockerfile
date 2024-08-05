FROM python:3.10.14-slim

WORKDIR /app

ENV PYTHONPATH=/app:$PYTHONPATH

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6

COPY . /app/

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
