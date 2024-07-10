aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 590183868930.dkr.ecr.us-east-2.amazonaws.com
docker build -t video_uploads .
docker tag video_uploads:latest 590183868930.dkr.ecr.us-east-2.amazonaws.com/video_uploads:latest
docker push 590183868930.dkr.ecr.us-east-2.amazonaws.com/video_uploads:latest