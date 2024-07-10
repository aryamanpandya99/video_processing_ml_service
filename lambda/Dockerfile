# Use the Amazon Linux 2 base image
FROM public.ecr.aws/lambda/python:3.10

# Copy the function code
COPY . ${LAMBDA_TASK_ROOT}

# COPY requirements.txt ./
# RUN pip install -r requirements.txt
EXPOSE 8080
# Command to run the Lambda function handler
CMD ["main.handler"]
