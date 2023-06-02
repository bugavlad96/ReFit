# https://www.youtube.com/watch?v=_GoXq9H0hqg
import threading

import mediapipe as mp
import cv2
import numpy as np
# import pyttsx3
import tests.voice_tests.voice as voice
import math
import threading
import libs.color_landmark as color
import libs.output_text as ot
import libs.compute_angle as ca

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

red =   (255, 0, 0)
green = (0, 255, 0)
blue =  (0, 0, 255)

# 12 - right shoulder
# 14 - right elbow
# 16 - right wrist
right_hand = [12, 14, 16]

# left_shoulder -> right_shouler -> right elbow
ls_rs_re = [11, 12, 14]

# for text output
first_lane = (150, 150)
second_lane = ()

while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 960))

    # Create CUDA-based OpenCV matrix
    d_img = cv2.cuda_GpuMat()
    d_img.upload(img)

    # Convert CUDA-based GpuMat to CPU-based numpy array
    img = d_img.download()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    # the condition will be True if at least one pose landmark is detected.
    # aici poti verifica daca faci displaty doar la landmark-urile relevante sau le lasi pe toate
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        points = {}
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            points[id] = (cx, cy)

        angle_deg_AC = ca.compute_angle(points, right_hand)
        ot.output_angle(img, points, 14, angle_deg_AC, red)
        angle_deg_DB = ca.compute_angle(points, ls_rs_re)
        ot.output_angle(img, points, 11, angle_deg_DB, red)

        print("Angle (degrees):", angle_deg_AC)

        #end test here
        if int(angle_deg_AC) >= 170 and points[20][1] > points[24][1] and counter == 0:
            color.color_landmark(img, points, right_hand, green)
            ot.output_text(img, "YOU CAN START THE EXERCISE", first_lane, green, 2)
            # cv2.putText(img, "YOU CAN START THE EXERCISE", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        elif int(angle_deg_AC) < 170:
            color.color_landmark(img, points, right_hand, blue)
            ot.output_text(img, "please extend your hand", first_lane, blue, 2)
            # cv2.putText(img, "please extend your hand", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        else:
            color.color_landmark(img, points, right_hand, green)
            if not up and int(angle_deg_DB) > 80 and int(angle_deg_DB) < 110:
                color.color_landmark(img, points, right_hand, green)
                if points[16][1] < points[5][1] and points[14][1] < points[5][1]:
                    print("it's UP")
                    up = True
                    counter += 1
                    print(counter)
                    color.color_landmark(img, points, right_hand, red)
                    # voice.speak("it's UP, great, now bring it down slowly")
            elif up and points[16][1] > points[24][1] and points[14][1] > points[12][1]:
                print("its down")
                up = False
                color.color_landmark(img, points, right_hand, red)
                # voice.speak("go up fast")
                # voice.speak("it's down, great, now bring it up slowly")
        print("--------------")


    ot.output_text(img, str(counter), first_lane, red, 12)
    # cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
