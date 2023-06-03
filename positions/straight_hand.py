import libs.color_landmark as color
import libs.output_text as ot
import libs.compute_angle as ca
import libs.global_var as var

# left - which hand to modify
# orientation - facing the camera or facing left to expose the right side, or right for left
# this function will include by default the printing of the angle on the stream, to check if to include it in the interface only or not
# will return the angles
#
def hand(left, body_desired_orientation, desired_shoulder_angle, desired_elbow_angle, permissible_angle_error, points, img):
    message = {actual_orientation: 0, actual_shoulder_angle: 0, actual_elbow_angle: 0,}
    if left:
        actual_orientation = ""
        if actual_orientation

        #   Decide on the shoulder angle
        actual_shoulder_angle = ca.compute_angle(points, var.LEFT_SHOULDER)
        actual_elbow_angle = ca.compute_angle(points, var.LEFT_HAND)
        message = {actual_orientation: 0, actual_shoulder_angle: 0, actual_elbow_angle: 0, }
        if desired_shoulder_angle - permissible_angle_error <= actual_shoulder_angle + permissible_angle_error:
            message += ""
        else:
    #         correct you r hand position to the desired one


    if not left:
        print()


