import libs.global_var as var
# import mediapipe as mp
# import cv2
from typing import List

# mpPose = mp.solutions.pose

# def is_point_visible(results, landmark_ids):
#     # Convert the frame to RGB format
#     # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#     # Initialize Mediapipe Pose
#     # pose = mpPose.Pose()
#
#     # Process the frame to detect pose landmarks
#     # results = pose.process(frame_rgb)
#
#     if results.pose_landmarks:
#         # Check if the specific landmark is visible
#         if results.pose_landmarks.landmark[landmark_id].visibility > 0.5:
#             return True
#         else:
#             return False
#     else:
#         return False

# -1 when no landmarks are visible
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
