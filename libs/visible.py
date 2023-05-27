import mediapipe as mp
import cv2

mpPose = mp.solutions.pose

def is_point_visible(frame, landmark_id):
    # Convert the frame to RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Initialize Mediapipe Pose
    pose = mpPose.Pose()

    # Process the frame to detect pose landmarks
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        # Check if the specific landmark is visible
        if results.pose_landmarks.landmark[landmark_id].visibility > 0.5:
            return True
        else:
            return False
    else:
        return False
