import mediapipe as mp
import cv2
import numpy as np
# import pyttsx3
import tests.voice_tests.voice as voice
import math
import libs.visible as visible

# Enable OpenCV to use CUDA
cv2.setUseOptimized(True)
cv2.cuda.setDevice(0)

# Create MediaPipe objects
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture(0)  # Use camera as the video source
up = False
counter = 0

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))

    # Create CUDA-based OpenCV matrix
    d_img = cv2.cuda_GpuMat()
    d_img.upload(img)

    # Convert CUDA-based GpuMat to CPU-based numpy array
    img = d_img.download()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        points = {}
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            points[id] = (cx, cy)

        # testing here
        # vector_AB = umar cot
        # vector_BC = cot incheietura 
        vector_DA = (points[11][0] - points[12][0], points[11][1] - points[12][1])
        vector_AB = (points[12][0] - points[14][0], points[12][1] - points[14][1])
        vector_BC = (points[14][0] - points[16][0], points[14][1] - points[16][1])
        

        # Calculate the dot product of AB and BC
        dot_product_DB = vector_DA[0] * vector_AB[0] + vector_DA[1] * vector_AB[1]
        dot_product_AC = vector_AB[0] * vector_BC[0] + vector_AB[1] * vector_BC[1]

        # Calculate the magnitudes of AB and BC
        magnitude_DA = math.sqrt(vector_DA[0] ** 2 + vector_DA[1] ** 2)
        magnitude_AB = math.sqrt(vector_AB[0] ** 2 + vector_AB[1] ** 2)
        magnitude_BC = math.sqrt(vector_BC[0] ** 2 + vector_BC[1] ** 2)

        # Calculate the cosine of the angle between AB and BC
        cosine_angle_DB = dot_product_DB / (magnitude_DA * magnitude_AB)
        cosine_angle_AC = dot_product_AC / (magnitude_AB * magnitude_BC)

        # Calculate the angle in radians
        angle_rad_DB = math.acos(cosine_angle_DB)
        angle_rad_AC = math.acos(cosine_angle_AC)

        # Convert the angle to degrees
        angle_deg_DB = math.degrees(angle_rad_DB)
        angle_deg_AC = math.degrees(angle_rad_AC)

        cv2.putText(img, str(int(angle_deg_AC)), (points[14][0], points[14][1]), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.putText(img, str(int(angle_deg_DB)), (points[12][0], points[12][1]), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        print("Angle (degrees):", angle_deg_AC)

        #end test here
        if int(angle_deg_AC) >= 0 and int(angle_deg_AC) <= 10:
            cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "YOU CAN START THE EXERCISE2 ", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), )
        else:
            cv2.circle(img, points[12], 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, points[14], 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, points[16], 15, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "please correct your hand extention, it must be fully extended 0 degrees", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), )


        if not up and points[22][1] < points[12][1]:
            print("UP")
            up = True
            counter += 1
            print(counter)
            # voice.speak("go down slowly")
        elif up and points[22][1] > points[12][1] and points[22][1] > points[24][1]:
            print("DOWN")
            up = False
            # voice.speak("go up fast")
        print("--------------")

    cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()