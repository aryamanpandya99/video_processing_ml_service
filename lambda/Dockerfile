FROM python:3.10

WORKDIR /app

# COPY requirements.txt /app/

RUN apt-get update && \
    apt-get install -y 

# RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["lambda_function.lambda_handler"]
