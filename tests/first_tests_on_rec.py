import mediapipe as mp
import cv2


mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture("curls.mkv")
up = False
counter = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280,720))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    # print("-----------------------------------")
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        points = {}
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            # print(id, lm, cx, cy)
            points[id] = (cx, cy)
        
        cv2.circle(img, points[22], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[12], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[21], 15, (255,0,0), cv2.FILLED)
        cv2.circle(img, points[11], 15, (255,0,0), cv2.FILLED)
        
        # daca right thumb e mai sus decat umarul drept atunci count += 1. nu uita ca originea 0,0 e in stanga sus colt
        if not up and points[22][1] < points[12][1]:
            print("UP")
            up = True
            counter += 1
            print(counter)
        # daca degetul mare e mai jos de umar si mai jos de bazin(24) atunci e down. incearca sa adaugi unghiuri
        elif up and points[22][1] > points[12][1] and points[22][1] > points[24][1]:
            print("DOWN")
            up = False
        print("--------------")
    
    cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255,0,0), 12)

    cv2.imshow("img", img)
    cv2.waitKey(1)