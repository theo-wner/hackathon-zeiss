from ultralytics import YOLO

model = YOLO("yolo-Weights/yolov8n-pose.pt")

# return a generator of Results objects
results = model.predict(source="0", stream=True)

for result in results:
    #boxes = result.boxes  # Boxes object for bounding box outputs
    #masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    #probs = result.probs  # Probs object for classification outputs
    #obb = result.obb  # Oriented boxes object for OBB outputs
    print(keypoints.xyn)

    result.show()  # display to screen






