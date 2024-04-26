import pyrealsense2 as rs
import numpy as np
import cv2

pipe = rs.pipeline()
cfg = rs.config()

cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  
cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30) 

pipe.start(cfg)

while True:
    frames = pipe.wait_for_frames()
    color_frame = frames.get_color_frame()
    depth_frame = frames.get_depth_frame()

    color_image = np.asanyarray(color_frame.get_data())
    depth_image = np.asanyarray(depth_frame.get_data())

    cv2.imshow("Color Image", color_image)
    cv2.imshow("Depth Image", depth_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

pipe.stop()