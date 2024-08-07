aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com
docker build -t video_uploads .
docker tag video_uploads:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/video_uploads:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-2.amazonaws.com/video_uploads:latest