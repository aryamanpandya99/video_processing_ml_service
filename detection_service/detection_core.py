"""
Object detection application.
In: s3 image paths
Out: detection values written to MongoDB

Author: Aryaman Pandya
"""

import io
import json

import boto3
import torch
from PIL import Image
from ultralytics import YOLO


def frames_from_paths(paths: list, is_aws: bool) -> list:
    """
    Given paths to images in s3, returns a torch tensor of
    these image frames stacked.

    Args:
        paths (list[str])
        is_aws (bool): whether paths are s3 paths or local

    Returns:
        frames (list[PIL.Image])
    """
    aws_client = boto3.client("s3")
    frames = []
    for path in paths:
        if is_aws:
            response = aws_client.get_object(Bucket="video-aws-bucket", Key=path)
            image_bytes = response["Body"].read()
            image = Image.open(io.BytesIO(image_bytes))
        else:
            image = Image.open(path)

        frames.append(image)  # YOLO takes care of the tensore conversion

    return frames


def object_detection(model, frames: torch.Tensor) -> list:
    """
    Runs the detection model on each frame and returns a list of result jsons

    Args:
        model: torch.nn.Module
        frames: torch.Tensor

    Returns:
        results: list[json]
    """
    return [json.loads(pred.tojson()) for pred in model.predict(frames, stream=True)]


def run_detection(frame_paths: list, is_aws: bool):
    """
    Runs the pipeline end to end: s3 paths -> write to db
    """
    print(frame_paths)
    frames = frames_from_paths([frame_paths], is_aws)
    model = YOLO(model="models/yolov9c.pt")
    if torch.cuda.is_available():
        model = model.to("cuda")

    predictions = object_detection(model, frames)
    print(predictions)
    return predictions
