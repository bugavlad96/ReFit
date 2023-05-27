import mediapipe as mp
import cv2
import voice_tests.voice

# Enable GPU acceleration in MediaPipe
mp.solutions.pose.Pose.use_gpu = True

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture(0)  # Use camera as the video source
up = False
counter = 0

with pose:
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (1280, 720))
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)

        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = {}
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                points[id] = (cx, cy)

            cv2.circle(img, points[22], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[12], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[21], 15, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, points[11], 15, (255, 0, 0), cv2.FILLED)

            if not up and points[22][1] < points[12][1]:
                print("UP")
                voice_tests.voice.speak("hai jos")
                up = True
                counter += 1
                print(counter)
            elif up and points[22][1] > points[12][1] and points[22][1] > points[24][1]:
                print("DOWN")
                voice_tests.voice.speak("hai sus")
                up = False
            print("--------------")

        cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
