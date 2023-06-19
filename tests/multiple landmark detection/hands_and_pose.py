import cv2
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands
mpPose = mp.solutions.pose

cap = cv2.VideoCapture(0)  # Use camera as the video source

with mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands, \
        mpPose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (1280, 960))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process hand landmarks
        hands_results = hands.process(imgRGB)
        if hands_results.multi_hand_landmarks:
            for hand_landmarks in hands_results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)

        # Process pose landmarks
        pose_results = pose.process(imgRGB)
        if pose_results.pose_landmarks:
            mpDraw.draw_landmarks(img, pose_results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        cv2.imshow("Hand and Pose Landmarks", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
