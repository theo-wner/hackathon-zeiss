from nxt_rest_connection import NXTRestConnection
from nxt_malibu_camera_handler import NXTMalibuCameraHandler
import cv2
from ultralytics import YOLO
from helper_functions import yield_pose_images
from final_gui import App

# Verbindung zur Kamera
rest_connection = NXTRestConnection(
    ip='169.254.75.124', username='admin', password='sdi')
camera_handler = NXTMalibuCameraHandler(rest_connection)

# Laden des Modells
model = YOLO("yolo-Weights/yolov8n-pose.pt")

# GUI
#app = App()

# Kamera-Stream
for img in yield_pose_images(camera_handler, model):
    cv2.imshow('Video', img)
    if cv2.waitKey(1) == ord('q'):
        break

# Aufräumen
cv2.destroyAllWindows()
