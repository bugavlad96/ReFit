import libs.utils as utils
import libs.compute_angle as ca
import libs.global_var as var
def left_foot(desired_knee_angle, permissible_angle_error, results, img, desired_hip_angle = None):

    # now check if the angle is right
    points = utils.collect_points(img, results)
    actual_knee_angle = ca.compute_angle(points, var.LEFT_FOOT)
    if desired_knee_angle - permissible_angle_error <= actual_knee_angle <= desired_knee_angle + permissible_angle_error:
        print("left KNEE angle - GOOD")
        if desired_hip_angle and (desired_hip_angle is not None) :
            # if parameter exists
            actual_hip_angle = ca.compute_angle(points, var.LEFT_HIP)
            print(f"({desired_hip_angle - permissible_angle_error}) <= {actual_hip_angle} <= ({desired_hip_angle - permissible_angle_error})")
            if (desired_hip_angle - permissible_angle_error) <= actual_hip_angle <= (desired_hip_angle + permissible_angle_error):
                print("left HIP angle - GOOD")
            else:
                print("left HIP angle - BAD")
    else:
        print("left KNEE angle - BAD")

def right_foot(desired_knee_angle, permissible_angle_error, results, img, desired_hip_angle = None):

    # now check if the angle is right
    points = utils.collect_points(img, results)
    actual_knee_angle = ca.compute_angle(points, var.RIGHT_FOOT)
    if desired_knee_angle - permissible_angle_error <= actual_knee_angle <= desired_knee_angle + permissible_angle_error:
        print("right KNEE angle - GOOD")
        if desired_hip_angle and (desired_hip_angle is not None) :
            # if parameter exists
            actual_hip_angle = ca.compute_angle(points, var.RIGHT_HIP)
            print(f"({desired_hip_angle - permissible_angle_error}) <= {actual_hip_angle} <= ({desired_hip_angle - permissible_angle_error})")
            if (desired_hip_angle - permissible_angle_error) <= actual_hip_angle <= (desired_hip_angle + permissible_angle_error):
                print("right HIP angle - GOOD")
            else:
                print("right HIP angle - BAD")
    else:
        print("right KNEE angle - BAD")