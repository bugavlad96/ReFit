# this method will color the relevant landmarks on live stream
import cv2

def color_landmark(img, points, color):
    for i in points:
        cv2.circle(img, points[i], 15, (0, 255, 0), cv2.FILLED)


