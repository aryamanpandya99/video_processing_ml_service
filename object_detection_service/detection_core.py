"""
Object detection application.
In: s3 image paths
Out: detection values written to MongoDB

Author: Aryaman Pandya
"""

import io
import json
from typing import Callable, List

import boto3
import torch
from PIL import Image
from ultralytics import YOLO


def get_local_image(path: str) -> Image.Image:
    """
    Fetch an image from a local path
    """
    return Image.open(path)


def get_aws_image(path: str, bucket: str) -> Image.Image:
    """
    Fetch an image from AWS S3
    """
    aws_client = boto3.client("s3")
    response = aws_client.get_object(Bucket=bucket, Key=path)
    image_bytes = response["Body"].read()
    return Image.open(io.BytesIO(image_bytes))


def frames_from_paths(
    paths: List[str], image_getter: Callable[[str], Image.Image]
) -> List[Image.Image]:
    """
    Given paths to images, returns a list of PIL Image objects.

    Args:
        paths (List[str]): List of image paths.
        image_getter (Callable[[str], Image.Image]): Function to get an image from a path.

    Returns:
        List[Image.Image]: List of PIL Image objects.
    """
    return [image_getter(path) for path in paths]


def predict_objects_in_frame(model, frames: torch.Tensor) -> list:
    """
    Runs the detection model on each frame and returns a list of result jsons

    Args:
        model: torch.nn.Module
        frames: torch.Tensor

    Returns:
        results: list[json]
    """
    return [json.loads(pred.tojson()) for pred in model.predict(frames, stream=True)]


def detections_from_img_paths(paths: List[str], is_aws: bool) -> list:
    """
    Driver function that runs detection end to end given a list of paths.
    Args:
        paths (List[str]): List of image paths.
        is_aws (bool): Flag indicating if the images are stored in AWS S3.

    Returns:
        predictions (list): List of predictions in JSON format.
    """
    image_getter = get_aws_image if is_aws else get_local_image
    frames = frames_from_paths(paths, image_getter)

    model = YOLO(model="models/yolov9c.pt")
    if torch.cuda.is_available():
        model = model.to("cuda")

    predictions = predict_objects_in_frame(model, frames)

    return predictions
