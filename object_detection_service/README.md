# Object Detection Service

This directory contains the code for an object detection service. The service is built using Flask and is designed to run object detection on frames provided through a POST request.

## Files

- `Dockerfile`: This file contains the instructions to build the Docker image for the object detection service.
- `detection-ingress.yml`: This file contains the Kubernetes Ingress configuration for the object detection service.
- `detection-k8s.yaml`: This file contains the Kubernetes Deployment and Service configurations for the object detection service.
- `app.py`: This file contains the main code for the object detection service.

## Usage

To use the object detection service locally for testing, use minikube and follow these steps:

1. Build the Docker image using the `Dockerfile`.
2. Deploy the Docker image to a Kubernetes cluster using the configurations in `detection-ingress.yml` and `detection-k8s.yaml`.
3. Send a POST request to the service with the frame to be processed. The frame should be included as a file in the `frame` field of the request.
4. The service will process the frame and return the detection results in JSON format.


### Build and Run

To build and run the object detection service, follow these steps:

1. Start minikube: `minikube start`

2. Enable the Ingress addon:
   ```
   minikube addons enable ingress
   ```

3. Set up your shell to use minikube's Docker daemon:
   ```
   eval $(minikube -p minikube docker-env)
   ```

4. Build the Docker image within minikube:
   ```
   docker build -t detection_container:latest .
   ```

5. Deploy the Kubernetes resources:
   ```
   kubectl apply -f detection-k8s.yaml
   ```

6. Apply the Ingress configuration:
   ```
   kubectl apply -f detection-ingress.yml
   ```

7. Wait for the Ingress to get an address:
   ```
   kubectl get ingress --watch
   ```

8. Add an entry to your /etc/hosts file:
   ```
   sudo echo "127.0.0.1 video-processing.com" | sudo tee -a /etc/hosts
   ```

9. Set up port forwarding to access the service:
   ```
   minikube tunnel
   ```

Now the object detection service is up and running within your minikube cluster. You can send a POST request to `http://video-processing.com/process` with the frame to be processed. The frame should be included as a file in the `frame` field of the request. The service will process the frame and return the detection results in JSON format.


## Deployment to AWS EKS

```bash
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com
```

```bash
docker build -t object-detection .
```

```bash
docker tag object-detection:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/object-detection:latest
```

```bash
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/object-detection:latest
```