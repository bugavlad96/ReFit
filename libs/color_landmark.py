# this method will color the relevant landmarks on live stream
import cv2

def color_landmark(img, points, color_this_points, color_code):
    for i in color_this_points:
        cv2.circle(img, points[i], 15, (color_code[0], color_code[1], color_code[2]), cv2.FILLED)
        print(f"cv2.circle(img, points[{i}], 15, (0, 255, 0), cv2.FILLED)")


