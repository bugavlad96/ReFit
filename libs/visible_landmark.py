import libs.global_var as var

def are_points_visible(results, landmark_ids):
    list = []
    visible = var.NOT_VISIBLE
    if results.pose_landmarks:
        for landmark_id in landmark_ids:
            # Check if the specific landmark is visible
            if results.pose_landmarks.landmark[landmark_id].visibility > 0.5:
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
