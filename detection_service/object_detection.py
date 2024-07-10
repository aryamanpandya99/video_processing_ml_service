"""
Object detection application. 
In: s3 image paths 
Out: detection values written to MongoDB

Author: Aryaman Pandya
"""
import argparse
import io
import json

import boto3
import torch
import torchvision.transforms.functional as F
from PIL import Image
from ultralytics import YOLO


def frames_from_s3_paths(
    s3_paths: list,
) -> torch.Tensor:
    """
    Given paths to images in s3, returns a torch tensor of
    these image frames stacked.

    Args:
        s3_paths (list[str])
    Returns:
        stacked_frames (torch.Tensor)
    """
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


def main(frame_paths: list):
    """
    Runs the pipeline end to end: s3 paths -> write to db
    """
    frames = frames_from_s3_paths(frame_paths)
    model = YOLO("yolov9c")
    if torch.cuda.is_available():
        model = model.to("cuda")

    predictions = object_detection(model, frames)
    print(predictions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--paths', nargs='+', help='List of s3 paths', required=True)
    args = parser.parse_args()

    main(args.paths)
