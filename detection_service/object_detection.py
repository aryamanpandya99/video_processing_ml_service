import json
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import io
import torch
import boto3
import torchvision.transforms.functional as F


def frames_from_s3_paths(
    s3_paths: list,
) -> list:
    s3 = boto3.client("s3")
    stacked_frames = None

    for path in s3_paths:
        response = s3.get_object(Bucket="video-aws-bucket", Key=path)
        image_bytes = response["Body"].read()
        image = Image.open(io.BytesIO(image_bytes))
        frame = F.pil_to_tensor(image)

        if stacked_frames is None:
            stacked_frames = frame.unsqueeze(0)  # Add batch dimension
        else:
            stacked_frames = torch.cat((stacked_frames, frame.unsqueeze(0)), dim=0)

    return stacked_frames


def object_detection(model, frames: list) -> list:
    return [json.loads(pred.tojson()) for pred in model.predict(frames, stream=True)]


def main():
    model = YOLO("yolov9c")
    if torch.cuda.is_available():
        model = model.to("cuda")
    frames = ["frame1.jpg", "frame2.jpg"]
    predictions = object_detection(model, frames)
    print(predictions)


if __name__ == "__main__":
    main()
