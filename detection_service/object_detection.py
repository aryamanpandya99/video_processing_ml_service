import json
from ultralytics import YOLO

def object_detection(model, frames: list) -> list:
    return [json.loads(pred.tojson()) for pred in model.predict(frames, stream=True)]

def main():
    model = YOLO('yolov9c')
    frames = ['frame1.jpg', 'frame2.jpg']
    predictions = object_detection(model, frames)
    print(predictions)

if __name__=='__main__':
    main()