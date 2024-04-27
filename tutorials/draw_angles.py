import cv2
import numpy as np
import random

# three random points
p1 = (random.randint(0, 400), random.randint(0, 400))
p2 = (random.randint(0, 400), random.randint(0, 400))
p3 = (random.randint(0, 400), random.randint(0, 400))

angle_threshold = 45

# calculate the angle on p2
angle = np.arctan2(p3[1] - p2[1], p3[0] - p2[0]) - np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
angle = np.degrees(angle)

# calculate the angle on p2, always positive, and draw the smaller angle
if angle < 0:
    angle = 360 + angle

if angle > 180:
    angle = 360 - angle
    #swap the points
    p1_new = p3
    p3_new = p1
    p1 = p1_new
    p3 = p3_new


#empty image
img = np.zeros((400, 400, 3), dtype=np.uint8)

# draw the points
cv2.circle(img, p1, 5, (255, 0, 0), -1)  # blue circle
cv2.circle(img, p2, 5, (0, 255, 0), -1)  # green circle
cv2.circle(img, p3, 5, (0, 0, 255), -1)  # red circle

# draw the lines
if angle < angle_threshold:
    cv2.line(img, p1, p2, (0, 0, 255), 1)  # red line
    cv2.line(img, p2, p3, (0, 0, 255), 1)  # red line
    cv2.line(img, p3, p1, (0, 0, 255), 1)  # red line
else:
    cv2.line(img, p1, p2, (0, 255, 0), 1)  # green line
    cv2.line(img, p2, p3, (0, 255, 0), 1)  # green line
    cv2.line(img, p3, p1, (0, 255, 0), 1)  # green line

# draw the oriented arc between the lines start at line p1-p2 and end at line p2-p3
if angle < angle_threshold:
    cv2.ellipse(img, p2, (50, 50), 0, np.degrees(np.arctan2(p1[1] - p2[1], p1[0] - p2[0])), np.degrees(np.arctan2(p3[1] - p2[1], p3[0] - p2[0])), (0, 0, 255), 1)  # red arc
else:
    cv2.ellipse(img, p2, (50, 50), 0, np.degrees(np.arctan2(p1[1] - p2[1], p1[0] - p2[0])), np.degrees(np.arctan2(p3[1] - p2[1], p3[0] - p2[0])), (0, 255, 0), 1)  # green arc

cv2.imshow('angle', img)
#close window on pressing any key
cv2.waitKey(0)
cv2.destroyAllWindows()


