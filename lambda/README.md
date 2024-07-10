# s3 Upload Triggered Lambda 

This subdir contains the definition of the container run by the lambda function that will be triggered when a new image has been uploaded to our s3 bucket. 

The lambda function is enabled by utilizing an ECR (Elastic Container Registry) container. To build the container, we use a Dockerfile that specifies the necessary dependencies and configurations. Once the container is built, we push it to the ECR repository using. This ensures that the container is available for execution when a new image is uploaded to our S3 bucket.

For ease of use, run the following to build and deploy. The current URL points to my private AWS account, be sure to replace those details to reproduce. 

```bash
chmod +x deploy_aws.sh
./deploy_aws.sh
```