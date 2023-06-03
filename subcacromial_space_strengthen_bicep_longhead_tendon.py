# https://www.youtube.com/watch?v=432yWPJQ-is  min:5:29
import threading

import mediapipe as mp
import cv2
import numpy as np
# import pyttsx3
import tests.voice_tests.voice as voice
import math
import libs.visible_landmark as visible
import libs.color_landmark as color
import libs.output_text as ot
import libs.compute_angle as ca
import libs.global_var as var

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
extended = False

while True:
    success, img = cap.read()
    # The default resolution that the models in the MediaPipe library were trained on is 640x480
    img = cv2.resize(img, var.STREAM_RESIZE)

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

        angle_deg_AC = ca.compute_angle(points, var.RIGHT_HAND)
        ot.output_angle(img, points, var.RIGHT_HAND[1], angle_deg_AC, var.BLUE)

        # print("Angle (degrees):", angle_deg_AC)


        if int(angle_deg_AC) >= 170 and points[20][1] > points[24][1] and counter == 0:
            color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
            ot.output_text(img, "YOU CAN START THE EXERCISE", var.FISRT_LANE,
                           var.GREEN, var.SIZE_TXT_HINTS)
        elif not up:
            if int(angle_deg_AC) >= 170 and points[20][1] > points[24][1] and counter > 0:
                color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
                ot.output_text(img, "great, it's down, now bring it up slowly", var.FISRT_LANE,
                               var.GREEN, var.SIZE_TXT_HINTS)
            elif (int(angle_deg_AC) < 170 and int(angle_deg_AC) > 100) or (int(angle_deg_AC) < 80):
                color.color_landmark(img, points, var.RIGHT_HAND, var.RED)
                ot.output_text(img, "elbow angle must be ~90 deg", var.FISRT_LANE,
                               var.RED, var.SIZE_TXT_HINTS)
            if points[14][1] > points[12][1] and  int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:
                color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
                ot.output_text(img, "~90 angle, good to go", var.FISRT_LANE,
                               var.GREEN, var.SIZE_TXT_HINTS)
            elif points[16][1] < points[12][1] and abs(points[14][1] - points[12][1]) <= 50 and int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:
                up = True
                counter += 1
                print(counter)
                # voice.speak("it's UP, great, now bring it down slowly")
                color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
                ot.output_text(img, "great, it's up", var.FISRT_LANE,
                               var.GREEN, var.SIZE_TXT_HINTS)
        elif up:
            if points[16][1]+30 < points[14][1] and int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:
                color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
                ot.output_text(img, "go down slowly", var.FISRT_LANE,
                               var.GREEN, var.SIZE_TXT_HINTS)
            elif points[16][1]+15 < points[14][1] and ((int(angle_deg_AC) < 80) or (int(angle_deg_AC) > 100)):
                color.color_landmark(img, points, var.RIGHT_HAND, var.RED)
                ot.output_text(img, "elbow angle must be ~90 deg", var.FISRT_LANE,
                               var.RED, var.SIZE_TXT_HINTS)
            if abs(points[14][1] - points[16][1]) <= 30 and int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:
                color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
                ot.output_text(img, "great, now extend the hand", var.FISRT_LANE,
                               var.GREEN, var.SIZE_TXT_HINTS)
                extended = True
            elif (points[16][1]+15 >= points[14][1] and int(angle_deg_AC) > 100) and not(extended):
                color.color_landmark(img, points, var.RIGHT_HAND, var.RED)
                ot.output_text(img, "get back to top position, and  ~90 deg", var.FISRT_LANE,
                               var.RED, var.SIZE_TXT_HINTS)
            elif points[16][1]+30 >= points[14][1] and int(angle_deg_AC) > 100 and extended:
                color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
                if int(angle_deg_AC) >= 170 and points[20][1] > points[24][1]:
                    print("its down")
                    up = False
                    extended = False
                    # # voice.speak("go up fast")
                    # # voice.speak("it's down, great, now bring it up slowly")
                    color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
                    ot.output_text(img, "great, it's down, now bring it up slowly", var.FISRT_LANE,
                                   var.GREEN, var.SIZE_TXT_HINTS)

        print("--------------")
    ot.output_text(img, str(counter), var.FISRT_LANE, var.BLUE, var.SIZE_TXT_KEY)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
