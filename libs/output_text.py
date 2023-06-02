# this method will color the relevant landmarks on live stream
import cv2

def output_angle(img, points, text_location, angle_value, color_code):
    cv2.putText(img, str(int(angle_value)), (points[text_location][0], points[text_location][1]), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
