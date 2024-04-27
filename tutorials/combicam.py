import cv2
import json
from ultralytics import YOLO
import torch
import numpy as np

# YOLO-Modell initialisieren
model = YOLO("yolo-Weights/yolov8n-pose.pt")

source = "0"
results = model.predict(source=source, stream=True)

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.4
color = (255, 255, 255)  # Weiß für die Nummerierung
thickness = 1
line_color = (0, 0, 255)  # Rot für die Linien
line_thickness = 2
angle_text = "Angle: N/A"

# Verbindungen, die gezeichnet werden sollen (0-basierte Indizes)
connections = [(10, 8), (8, 6), (6, 12), (12, 11), (11, 5), (5, 6), (5, 7), (7, 9), (12, 14),
               (14, 16), (11, 13), (13, 15), (4, 2), (2, 1), (1, 3), (0, 4), (3, 0), (4, 6), (3, 5)]

frame_count = 0
for result in results:
    keypoints = result.keypoints
    data_list = keypoints.xyn.cpu().numpy().tolist()
    tensors = [torch.tensor(data, dtype=torch.float32) for data in data_list]

    img_size = (640, 480)
    image = torch.zeros(
        (img_size[1], img_size[0], 3), dtype=torch.uint8).numpy()

    points = []  # List to hold point coordinates

    for tensor in tensors:
        current_points = [(int(p[0] * img_size[0]), int(p[1] * img_size[1]))
                          for p in tensor]
        points.extend(current_points)
        for i, (x, y) in enumerate(current_points):
            if x > 0 and y > 0:
                cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
                cv2.putText(image, str(i + 1), (x + 6, y + 6),
                            font, font_scale, color, thickness)

    # Draw connections
    for start_idx, end_idx in connections:
        if start_idx < len(points) and end_idx < len(points):
            start_point = points[start_idx]
            end_point = points[end_idx]
            if start_point[0] > 0 and start_point[1] > 0 and end_point[0] > 0 and end_point[1] > 0:
                cv2.line(image, start_point, end_point,
                         line_color, line_thickness)

    # Calculate angle between vectors
    if len(points) > 16:  # Check if there are enough points
        # Vector from 12 to 14
        v1 = np.array(points[13]) - np.array(points[11])
        # Vector from 14 to 16
        v2 = np.array(points[15]) - np.array(points[13])
        if np.all(v1) and np.all(v2):  # Check if points are not zero
            unit_v1 = v1 / np.linalg.norm(v1)
            unit_v2 = v2 / np.linalg.norm(v2)
            dot_product = np.dot(unit_v1, unit_v2)
            angle = np.arccos(dot_product) * (180 / np.pi)
            angle_text = f"Angle: {angle:.2f}°"
            print(f"Angle between 12-14 and 14-16: {angle:.2f} degrees")
        else:
            print("Angle calculation not possible, missing points.")
    else:
        print("Not enough points for angle calculation.")

     # Display angle
    cv2.putText(image, angle_text, (10, 30), font,
                font_scale, color, thickness)

    # Display the image
    cv2.imshow('YOLO Keypoints Visualization', image)
    if cv2.waitKey(1) == ord('q') or frame_count >= 10000:
        break
    frame_count += 1

model.close()
cv2.destroyAllWindows()
