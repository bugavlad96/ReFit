import cv2
import mediapipe as mp

mpDraw = mp.solutions.drawing_utils
mpHands = mp.solutions.hands

cap = cv2.VideoCapture(0)  # Use camera as the video source

with mpHands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands:
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process hand landmarks
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)

        cv2.imshow("Hand Landmarks", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
