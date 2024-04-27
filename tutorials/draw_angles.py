import cv2
import numpy as np
import random

'''
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

'''
def draw_angle(points, interest_index, angle_threshold, draw_points=False, draw_green_lines=False):
    pts = [point for point in points if points.index(point) in interest_index]
    p1, p2, p3 = pts[0], pts[1], pts[2]


    #angle at p2
    angle = np.arctan2(p3[1] - p2[1], p3[0] - p2[0]) - np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
    angle = np.degrees(angle)
    if angle < 0:
        angle = abs(angle)


    if angle > 180:
        angle = 360 - angle
        
    img = np.zeros((400, 400, 3), dtype=np.uint8)

    # draw the points
    if draw_points:
        cv2.circle(img, p1, 5, (255, 0, 0), -1)  # blue circle  
        cv2.circle(img, p2, 5, (0, 255, 0), -1)  # green circle
        cv2.circle(img, p3, 5, (0, 0, 255), -1)  # red circle

    # draw the lines
    if angle < angle_threshold:
        cv2.line(img, p1, p2, (0, 0, 255), 1)  # red line
        cv2.line(img, p2, p3, (0, 0, 255), 1)  # red line
        cv2.line(img, p3, p1, (0, 0, 255), 1)  # red line

    elif draw_green_lines:
        cv2.line(img, p1, p2, (0, 255, 0), 1)  # green line
        cv2.line(img, p2, p3, (0, 255, 0), 1)  # green line
        cv2.line(img, p3, p1, (0, 255, 0), 1)  # green line

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
        #put text small angle
        cv2.putText(img,str(round(small_angle)), (p2[0] + 10, p2[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img,str(round(big_angle)), (p2[0] + 10, p2[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if start_angle >180:
            start_angle = start_angle - 360
        if end_angle > 180:
            end_angle = end_angle - 360
        

    if angle < angle_threshold:
        cv2.ellipse(img, p2, (50, 50), 0, start_angle, end_angle, (0, 0, 255), 1)
    else:
        cv2.ellipse(img, p2, (50, 50), 0, start_angle, end_angle, (0, 255, 0), 1)

        
    #draw angle value
    cv2.putText(img, str(round(angle, 2)), (p2[0] + 10, p2[1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow('angle', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #create random 20 points
    points = [(random.randint(0, 400), random.randint(0, 400)) for _ in range(20)]
    points = [(66, 36), (145, 105), (259, 376)]
    draw_angle(points, [0,1,2], 45, draw_points=True, draw_green_lines=True)
    