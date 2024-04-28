from nxt_rest_connection import NXTRestConnection
from nxt_malibu_camera_handler import NXTMalibuCameraHandler
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from pygame import mixer

def draw_keypoints(img, yolo_results):
    # Konfiguration der Zeichenfunktion
    font=cv2.FONT_HERSHEY_SIMPLEX
    font_scale=0.4
    color=(255, 255, 255)
    thickness=1
    line_color=(0, 255, 0)
    line_thickness=2
    connections=[(10, 8), (8, 6), (6, 12), (12, 11), (11, 5), (5, 6), (5, 7), (7, 9), (4, 2), (2, 1), (1, 3), (0, 4), (3, 0), (4, 6), (3, 5)]

    # Plotte Punkte und Verbindungen
    for result in yolo_results:
        if result is not None:
            keypoints = result.keypoints
            data_list = keypoints.xyn.cpu().numpy().tolist()
            for person in data_list:
                points = [(int(p[0] * img.shape[1]),
                            int(p[1] * img.shape[0])) for p in person]
                
                print(points)

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
                            
                # Zeichne Winkel
                img = draw_angle(img, points, [12, 14, 16], 90, draw_points=False, line_thickness=line_thickness)
                img = draw_angle(img, points, [11, 13, 15], 90, draw_points=False, line_thickness=line_thickness)
    return img


def draw_angle(img, points, interest_index, angle_threshold, draw_points=False, line_thickness=1):
    mixer.init()
    interest_index = np.array(interest_index, dtype=int)
    pts = [point for idx,point in enumerate(points) if idx in interest_index]
    if (0,0) in pts:
        return img
    p1, p2, p3 = pts[0], pts[1], pts[2]


    #angle at p2
    angle = np.arctan2(p3[1] - p2[1], p3[0] - p2[0]) - np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
    angle = np.degrees(angle)
    if angle < 0:
        angle = abs(angle)


    if angle > 180:
        angle = 360 - angle

    # draw the points
    if draw_points:
        cv2.circle(img, p1, 5, (255, 0, 0), line_thickness)  # blue circle  
        cv2.circle(img, p2, 5, (0, 255, 0), line_thickness)  # green circle
        cv2.circle(img, p3, 5, (0, 0, 255), line_thickness)  # red circle

    # draw the lines
    if angle < angle_threshold:
        cv2.line(img, p1, p2, (0, 0, 255), line_thickness)  # red line
        cv2.line(img, p2, p3, (0, 0, 255), line_thickness)  # red line
        cv2.line(img, p3, p1, (0, 0, 255), line_thickness)  # red line
        plays=mixer.Sound("../sounds/token.mpeg")
        plays.play()

    else:
        cv2.line(img, p1, p2, (0, 255, 0), line_thickness)  # green line
        cv2.line(img, p2, p3, (0, 255, 0), line_thickness)  # green line
        cv2.line(img, p3, p1, (0, 255, 0), line_thickness)  # green line

    # draw the oriented arc between the lines start at line p1-p2 and end at line p2-p3
    angle_p1_p2 = np.degrees(np.arctan2(p1[1] - p2[1], p1[0] - p2[0]))
    angle_p3_p2 = np.degrees(np.arctan2(p3[1] - p2[1], p3[0] - p2[0]))
    
    if angle_p1_p2 < 0:
        angle_p1_p2 += 360
    if angle_p3_p2 < 0:
        angle_p3_p2 += 360

    small_angle = min(angle_p1_p2, angle_p3_p2) 
    big_angle = max(angle_p1_p2, angle_p3_p2)

    if big_angle - small_angle < 180:
        start_angle = small_angle
        end_angle = big_angle
    else:
        start_angle = big_angle
        end_angle = small_angle  

        if start_angle >180:
            start_angle = start_angle - 360
        if end_angle > 180:
            end_angle = end_angle - 360
        

    if angle < angle_threshold:
        cv2.ellipse(img, p2, (50, 50), 0, start_angle, end_angle, (0, 0, 255), 1)
    else:
        cv2.ellipse(img, p2, (50, 50), 0, start_angle, end_angle, (0, 255, 0), 1)

        
    #draw angle value
    cv2.putText(img, str(round(angle, 2)), (p2[0] + 10, p2[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    return img

def yield_pose_images(camera_handler, model):
    frame_count = 0
    while True:
        img = camera_handler.get_image()
        img = Image.open(BytesIO(img))
        img = np.array(img)
        # downscale image to 720p
        img = cv2.resize(img, (1280, 720))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if frame_count % 1 == 0:
            results = model(img, stream=True)
            try:
                img = draw_keypoints(img, results)
            except:
                pass

        yield img