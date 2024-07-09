FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && \
    apt-get install -y 

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# format necessary to allow display to work
ENV DISPLAY=:99
CMD ["python", "lambda_function.py"]
