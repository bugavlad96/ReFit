import mediapipe as mp
import cv2
import libs.visible_landmark as vl
import libs.global_var as var
# config_path = r"config.pbtxt"

# Create a MediaPipe pipeline with the configuration file
# pipeline = mp.CalculatorGraph(config=config_path)

# Run the pipeline
# pipeline.run()


mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture(0)  # Use camera as the video source
up = False
counter = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, var.STREAM_RESIZE)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    print(vl.are_points_visible(results, var.EXPOSED_FRONT))

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
            up = True
            counter += 1
            print(counter)
        elif up and points[22][1] > points[12][1] and points[22][1] > points[24][1]:
            print("DOWN")
            up = False
        print("--------------")

    cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
