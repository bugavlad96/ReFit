# https://youtu.be/nX7ydOeNsoM?t=103

# https://youtu.be/nX7ydOeNsoM?t=86


# https://www.youtube.com/watch?v=432yWPJQ-is  min:5:29
import threading

import mediapipe as mp
import cv2
import numpy as np
# import pyttsx3
import tests.voice_tests.voice as voice
import math
import libs.visible_landmark as visible
import threading
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
left_up = False
right_up = False
counter_left = 0
counter_right = 0
ready = False
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

        angle_deg_AC = ca.compute_angle(points, var.LEFT_FOOT)
        angle_deg_EG = ca.compute_angle(points, var.RIGHT_FOOT)
        ot.output_angle(img, points, var.LEFT_FOOT[1], angle_deg_AC, var.RED)
        ot.output_angle(img, points, var.RIGHT_FOOT[1], angle_deg_EG, var.RED)

        # print("Angle (degrees):", angle_deg_AC)

        if (int(angle_deg_AC) >= 165 and int(angle_deg_EG) >= 165) and (counter_left == counter_right == 0):
            color.color_landmark(img, points, var.LEFT_FOOT, var.GREEN)
            color.color_landmark(img, points, var.RIGHT_FOOT, var.GREEN)
            ot.output_text(img, "Great, now, begin the exercise :), bring both your knees up ", var.FISRT_LANE, var.GREEN, var.SIZE_TXT_HINTS)
        elif (int(angle_deg_AC) >= 165 and int(angle_deg_EG) >= 165) and (counter_left == counter_right != 0):
            color.color_landmark(img, points, var.LEFT_FOOT, var.GREEN)
            color.color_landmark(img, points, var.RIGHT_FOOT, var.GREEN)
            ot.output_text(img, "good job, now go up again....", var.FISRT_LANE, var.GREEN, var.SIZE_TXT_HINTS)
            left_up = False
            right_up = False
        elif not (left_up and right_up) and (int(angle_deg_AC) < 165 and int(angle_deg_EG) < 165):
            color.color_landmark(img, points, var.LEFT_FOOT, var.BLUE)
            color.color_landmark(img, points, var.RIGHT_FOOT, var.BLUE)
            ot.output_text(img, "a little more...", var.FISRT_LANE, var.BLUE, var.SIZE_TXT_HINTS)
            if int(angle_deg_AC) < 65 and int(angle_deg_EG) < 65:
                left_up = True
                right_up = True
                counter_left += 1
                counter_right += 1
                # print(counter)
                # voice.speak("it's UP, great, now bring it down slowly")
                color.color_landmark(img, points, var.LEFT_FOOT, var.RED)
                color.color_landmark(img, points, var.RIGHT_FOOT, var.RED)
                ot.output_text(img, "great, it's up. Now go down slowly in a controlled way, extend fully your feet", var.FISRT_LANE, var.GREEN, var.SIZE_TXT_HINTS)
        elif (left_up and right_up):
            if (int(angle_deg_AC) < 65 and int(angle_deg_EG) < 65):
                color.color_landmark(img, points, var.LEFT_FOOT, var.RED)
                color.color_landmark(img, points, var.RIGHT_FOOT, var.RED)
                ot.output_text(img, "great, it's up. Now go down slowly in a controlled way, extend fully your feet",
                               var.FISRT_LANE, var.GREEN, var.SIZE_TXT_HINTS)
            if (int(angle_deg_AC) > 65 and int(angle_deg_EG) > 65) and (int(angle_deg_AC) <= 165 and int(angle_deg_EG) <= 165):
                color.color_landmark(img, points, var.LEFT_FOOT, var.BLUE)
                color.color_landmark(img, points, var.RIGHT_FOOT, var.BLUE)
                ot.output_text(img, "try to bring SLOWLY your knees as close as possible to the ground...",
                               var.FISRT_LANE, var.BLUE, var.SIZE_TXT_HINTS)

        print("--------------")


    ot.output_text(img, str(counter_left), var.FISRT_LANE, var.RED, var.SIZE_TXT_KEY)
    ot.output_text(img, str(counter_right), var.FISRT_LANE_SECOND_COUTER, var.RED, var.SIZE_TXT_KEY)



    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
