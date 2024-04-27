from ultralytics import YOLO
#from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2

model = YOLO("yolo-Weights/yolov8n-pose.pt")

results = model.predict(source="0", show=True)

print(results)

for r in results:
    boxes = r.boxes
    keypoints = r.keypoints
    print("Keypoints --->")
    print(keypoints)
