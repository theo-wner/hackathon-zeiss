from nxt_rest_connection import NXTRestConnection
from nxt_malibu_camera_handler import NXTMalibuCameraHandler
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from ultralytics import YOLO
import torch

rest_connection = NXTRestConnection(ip='169.254.75.124', username='admin', password='sdi')

camera_handler = NXTMalibuCameraHandler(rest_connection)

# model
model = YOLO("yolo-Weights/yolov8n-pose.pt")

# Font and stuff
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

# Initialize variables
keypoints = None
frame_count = 0

while True:
    img = camera_handler.get_image()
    img = Image.open(BytesIO(img))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # only update every x frames
    if frame_count % 1 == 0:
        results = model(img, stream=True)
        if results is not None:
            # coordinates
            for r in results:
                keypoints = r.keypoints
    
    # Pose estimation
    if keypoints is not None:
        data_list = keypoints.xyn.cpu().numpy().tolist()
        tensors = [torch.tensor(data, dtype=torch.float32) for data in data_list]

        img_size = (1920, 1080)
        image = torch.zeros(
            (img_size[1], img_size[0], 3), dtype=torch.uint8).numpy()

        points = []  # List to hold point coordinates

        for tensor in tensors:
            current_points = [(int(p[0] * img_size[0]), int(p[1] * img_size[1]))
                            for p in tensor]
            points.extend(current_points)
            for i, (x, y) in enumerate(current_points):
                if x > 0 and y > 0:
                    cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
                    cv2.putText(img, str(i + 1), (x + 6, y + 6),
                                font, font_scale, color, thickness)

        # Draw connections
        for start_idx, end_idx in connections:
            if start_idx < len(points) and end_idx < len(points):
                start_point = points[start_idx]
                end_point = points[end_idx]
                if start_point[0] > 0 and start_point[1] > 0 and end_point[0] > 0 and end_point[1] > 0:
                    cv2.line(img, start_point, end_point,
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

    cv2.imshow('Video', img)
    if cv2.waitKey(1) == ord('q'):
        break
