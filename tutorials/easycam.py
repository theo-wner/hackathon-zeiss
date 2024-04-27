import cv2
import json
from ultralytics import YOLO
import torch

model = YOLO("yolo-Weights/yolov8n-pose.pt")

source = "0"
results = model.predict(source=source, stream=True)

frame_count = 0

for result in results:
    keypoints = result.keypoints

    filename = f'txt/keypoints_data_{frame_count}.txt'

    with open(filename, 'w') as f:
        data_list = keypoints.xyn.cpu().numpy().tolist()
        json.dump(data_list, f)

    frame_count += 1

    result.show()

    if frame_count >= 10:
        break

model.close()
