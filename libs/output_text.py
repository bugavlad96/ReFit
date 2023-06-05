# this method will color the relevant landmarks on live stream
import cv2
import libs.global_var as var

# dict_with_values cirespunde cu structura returnata de functia step
def output_angles(img, points, dict_with_values, color_code):

    if dict_with_values is not None:
        # example or a dict record: key = "LEFT_HAND", value = [var.LEFT_HAND, [False, 180grade]]
        for body_part_txt, (body_part_array, angle) in dict_with_values.items():
                cv2.putText(img, str(int(angle[1])), (points[body_part_array[1]][0], points[body_part_array[1]][1]), cv2.FONT_HERSHEY_PLAIN, var.SIZE_ANGLES, color_code, var.SIZE_ANGLES)

            # cv2.putText(img, str(int(angle[1])), (points[body_part_array[1]][0], points[body_part_array[1]][1]), cv2.FONT_HERSHEY_PLAIN, var.SIZE_ANGLES, color_code, var.SIZE_ANGLES)


# def output_angles(img, points, angle_location, angle_value, color_code):
#     cv2.putText(img, str(int(angle_value)), (points[angle_location][0], points[angle_location][1]),
#                 cv2.FONT_HERSHEY_PLAIN, var.SIZE_TXT_HINTS, var.SIZE_ANGLES, color_code, var.SIZE_ANGLES)


def output_text(img, text, text_location, color_code, size):
    cv2.putText(img, text, text_location, cv2.FONT_HERSHEY_PLAIN, size, (color_code[0], color_code[1], color_code[2]), size)
