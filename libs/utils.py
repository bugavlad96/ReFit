import libs.global_var as var
import libs.compute_angle as ca

def collect_points(img, results):
    points = {}
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            points[id] = (cx, cy)
    return points


# facing left, right or front
def body_orientation(desired_body_orientation, results, img):
    if are_points_visible(results, desired_body_orientation):
        print("BODY orientation - GOOD")
        return True
    else:
        print("BODY orientation - BAD")
        return False

# will take an array as input which represent two vectors with a common point where they coincide

def is_body_angle_correct(body_part, desired_angle, permissible_angle_error, points):

    actual_angle = ca.compute_angle(points, body_part)
    # print(f"({desired_angle - permissible_angle_error}) <= {actual_angle} <= ({desired_angle - permissible_angle_error})")
    if (desired_angle - permissible_angle_error) <= actual_angle <= (desired_angle + permissible_angle_error):
        print(f"body part: {var.find_variable_name(body_part)} with angle {actual_angle} - GOOD")
        return True
    else:
        print(f"body part: {var.find_variable_name(body_part)} with angle {actual_angle} - BAD")
        return False



def are_points_visible(results, landmark_ids):
    list = []
    visible = var.NOT_VISIBLE
    if results.pose_landmarks:
        for landmark_id in landmark_ids:
            # Check if the specific landmark is visible
            if results.pose_landmarks.landmark[landmark_id].visibility > 0.7:
                list.append(var.VISIBLE)
            else:
                list.append(var.NOT_VISIBLE)
                break

    if len(landmark_ids) == len(list):
        if list[len(list) - 1] == var.VISIBLE:
            return var.VISIBLE
        else:
            return var.NOT_VISIBLE
    else:
        return var.NOT_VISIBLE

def body_position(desired_body_orientation, results, img):
    # if facing front trebuie sa vad acele 4 puncte
    # if facing lateral nu trebuie sa fac jumatatea opusa
    # daca sunt culcat cum verific asta?

    if are_points_visible(results, desired_body_orientation):

        print("BODY orientation - GOOD")
        return True
    else:
        print("BODY orientation - BAD")
        return False
