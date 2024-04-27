from nxt_rest_connection import NXTRestConnection
from nxt_malibu_camera_handler import NXTMalibuCameraHandler
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from ultralytics import YOLO
import torch

rest_connection = NXTRestConnection(
    ip='169.254.75.124', username='admin', password='sdi')
camera_handler = NXTMalibuCameraHandler(rest_connection)

# Laden des Modells
model = YOLO("yolo-Weights/yolov8n-pose.pt")

# Schriftarten und Farben für die Darstellung
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.4
color = (255, 255, 255)  # Weiß
thickness = 1
line_color = (0, 0, 255)  # Rot
line_thickness = 2

# Verbindungen zwischen den Schlüsselpunkten
connections = [(10, 8), (8, 6), (6, 12), (12, 11), (11, 5), (5, 6), (5, 7), (7, 9), (12, 14),
               (14, 16), (11, 13), (13, 15), (4, 2), (2, 1), (1, 3), (0, 4), (3, 0), (4, 6), (3, 5)]

frame_count = 0

while True:
    img = camera_handler.get_image()
    img = Image.open(BytesIO(img))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if frame_count % 1 == 0:
        results = model(img, stream=True)
        for result in results:
            if result is not None:
                keypoints = result.keypoints
                data_list = keypoints.xyn.cpu().numpy().tolist()
                for person in data_list:
                    points = [(int(p[0] * img.shape[1]),
                               int(p[1] * img.shape[0])) for p in person]

                    # Zeichne Punkte und Nummerierungen
                    for idx, (x, y) in enumerate(points):
                        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
                        cv2.putText(img, str(idx + 1), (x + 6, y + 6),
                                    font, font_scale, color, thickness)

                    # Zeichne Verbindungen
                    for start_idx, end_idx in connections:
                        if start_idx < len(points) and end_idx < len(points):
                            start_point = points[start_idx]
                            end_point = points[end_idx]
                            if start_point[0] > 0 and start_point[1] > 0 and end_point[0] > 0 and end_point[1] > 0:
                                cv2.line(img, start_point, end_point,
                                         line_color, line_thickness)

    cv2.imshow('Video', img)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
