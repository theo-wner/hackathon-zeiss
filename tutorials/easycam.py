import cv2
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
        f.write(str(keypoints.xyn))

    frame_count += 1

    result.show()

    if frame_count >= 10:
        break

model.close()
