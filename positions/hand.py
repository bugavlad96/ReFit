import libs.compute_angle as ca
import libs.global_var as var
import libs.utils as utils
# orientation - will take a list of required landmarks from var.global_var. facing the camera or facing left to expose the right side, or right for left
# this function will include by default the printing of the angle on the stream, to check if to include it in the interface only or not
# will return the angles
#

# def body orientation:


def left_hand(desired_elbow_angle, permissible_angle_error, results, img, desired_shoulder_angle = None):

    # now check if the angle is right
    points = utils.collect_points(img, results)
    actual_elbow_angle = ca.compute_angle(points, var.LEFT_HAND)
    if desired_elbow_angle - permissible_angle_error <= actual_elbow_angle <= desired_elbow_angle + permissible_angle_error:
    #         do somthing
        print("left ELBOW angle - GOOD")
        if desired_shoulder_angle and (desired_shoulder_angle is not None) :
            # if parameter exists
            actual_shoulder_angle = ca.compute_angle(points, var.LEFT_SHOULDER)
            print(f"({desired_shoulder_angle - permissible_angle_error}) <= {actual_shoulder_angle} <= ({desired_shoulder_angle - permissible_angle_error})")
            if (desired_shoulder_angle - permissible_angle_error) <= actual_shoulder_angle <= (desired_shoulder_angle + permissible_angle_error):
                print("left SHOULDER angle - GOOD")
            else:
                print("left SHOULDER angle - BAD")


    else:
        print("left ELBOW angle - BAD")


def right_hand(desired_elbow_angle, permissible_angle_error, results, img, desired_shoulder_angle = None):

    # now check if the angle is right
    points = utils.collect_points(img, results)
    actual_elbow_angle = ca.compute_angle(points, var.RIGHT_HAND)
    if desired_elbow_angle - permissible_angle_error <= actual_elbow_angle <= desired_elbow_angle + permissible_angle_error:
    #         do somthing
        print("right ELBOW angle - GOOD")
        if desired_shoulder_angle and (desired_shoulder_angle is not None) :
            # if parameter exists
            actual_shoulder_angle = ca.compute_angle(points, var.RIGHT_SHOULDER)
            print(f"({desired_shoulder_angle - permissible_angle_error}) <= {actual_shoulder_angle} <= ({desired_shoulder_angle - permissible_angle_error})")
            if (desired_shoulder_angle - permissible_angle_error) <= actual_shoulder_angle <= (desired_shoulder_angle + permissible_angle_error):
                print("right SHOULDER angle - GOOD")
            else:
                print("right SHOULDER angle - BAD")


    else:
        print("right ELBOW angle - BAD")