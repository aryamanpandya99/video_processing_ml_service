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


def main(frames: list):
    model = YOLO("yolov9c")
    if torch.cuda.is_available():
        model = model.to("cuda")
    
    predictions = object_detection(model, frames)
    print(predictions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--paths', nargs='+', help='List of s3 paths', required=True)
    args = parser.parse_args()

    frames = frames_from_s3_paths(args.paths)
    main(frames)
