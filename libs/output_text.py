# this method will color the relevant landmarks on live stream
import cv2

def output_angle(img, points, angle_location, angle_value, color_code):
    cv2.putText(img, str(int(angle_value)), (points[angle_location][0], points[angle_location][1]), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)


def output_text(img, text, text_location, color_code, size):
    cv2.putText(img, text, text_location, cv2.FONT_HERSHEY_PLAIN, size, (color_code[0], color_code[1], color_code[2]), size)
