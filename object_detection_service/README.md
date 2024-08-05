# Object Detection Service

This directory contains the code for an object detection service. The service is built using Flask and is designed to run object detection on frames provided through a POST request.

## Files

- `Dockerfile`: This file contains the instructions to build the Docker image for the object detection service.
- `detection-ingress.yml`: This file contains the Kubernetes Ingress configuration for the object detection service.
- `detection-k8s.yaml`: This file contains the Kubernetes Deployment and Service configurations for the object detection service.
- `app.py`: This file contains the main code for the object detection service.

## Usage

To use the object detection service, follow these steps:

1. Build the Docker image using the `Dockerfile`.
2. Deploy the Docker image to a Kubernetes cluster using the configurations in `detection-ingress.yml` and `detection-k8s.yaml`.
3. Send a POST request to the service with the frame to be processed. The frame should be included as a file in the `frame` field of the request.
4. The service will process the frame and return the detection results in JSON format.
