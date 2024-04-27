from nxt_rest_connection import NXTRestConnection
from nxt_malibu_camera_handler import NXTMalibuCameraHandler
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

rest_connection = NXTRestConnection(ip='169.254.75.124', username='admin', password='sdi')

camera_handler = NXTMalibuCameraHandler(rest_connection)


for i in range(1000):
    image = camera_handler.get_image()

    image = Image.open(BytesIO(image))

    # Convert from PIL to OpenCV
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    cv2.imshow('Video', image)
    if cv2.waitKey(1) == ord('q'):
        break
