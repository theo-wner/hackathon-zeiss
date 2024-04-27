import cv2
from matplotlib import pyplot as plt
from nxt_rest_connection import NXTRestConnection
from nxt_malibu_camera_handler import NXTMalibuCameraHandler
from ultralytics import YOLO
from PIL import Image
from helper_functions import yield_pose_images

from final_gui import App

# Verbindung zur Kamera
rest_connection = NXTRestConnection(
    ip='169.254.75.124', username='admin', password='sdi')
camera_handler = NXTMalibuCameraHandler(rest_connection)

# Laden des Modells
model = YOLO("yolo-Weights/yolov8n-pose.pt")

# GUI initialisieren
app = App()

for img in yield_pose_images(camera_handler, model):
    app.update()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    app.change_image(img)

    # cv2.imshow('Video', img) # this does not work 
    # cv2.imwrite('test.jpg', img)  # this works! 

# # Kamera-Stream
# for img in yield_pose_images(camera_handler, model):
#     cv2.imshow('Video', img)
#     if cv2.waitKey(1) == ord('q'):
#         break

# # Aufräumen
# cv2.destroyAllWindows()
