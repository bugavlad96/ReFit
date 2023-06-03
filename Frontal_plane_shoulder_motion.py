# https://www.youtube.com/watch?v=_GoXq9H0hqg

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
import libs.global_var as var
import libs.prepare_stream_BGR2RGB as ps
import libs.utils as utils
import positions.hand as hand
import positions.body as body

# Enable OpenCV to use CUDA
cv2.setUseOptimized(True)
cv2.cuda.setDevice(0)

# Create MediaPipe objects
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

cap = cv2.VideoCapture(0)  # Use camera as the video source
# intantiate some vars
up = False
counter = 0

while True:

    img, results = ps.prepare_stream(cap, pose)

    # the condition will be True if at least one pose landmark is detected.
    # aici poti verifica daca faci displaty doar la landmark-urile relevante sau le lasi pe toate
    if results.pose_landmarks:
        # printeaza punctele si conexiunile. Oferit de mdedia pipe
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        points = utils.collect_points(img, results)

        print(body.body(var.EXPOSED_FRONT, results, img))
        print(hand.left_hand(90, 10, results, img, 180))
        print(hand.right_hand(90, 10, results, img, 180))

        # compute the angles
        angle_deg_AC = ca.compute_angle(points, var.RIGHT_HAND)
        ot.output_angle(img, points, 14, angle_deg_AC, var.RED)

        angle_deg_DB = ca.compute_angle(points, var.RIGHT_SHOULDER)
        ot.output_angle(img, points, 11, angle_deg_DB, var.RED)

        if int(angle_deg_AC) >= 170 and points[20][1] > points[24][1] and counter == 0:
            color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
            ot.output_text(img, "YOU CAN START THE EXERCISE", var.FISRT_LANE, var.GREEN, var.SIZE_TXT_HINTS)
            # cv2.putText(img, "YOU CAN START THE EXERCISE", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        elif int(angle_deg_AC) < 170:
            color.color_landmark(img, points, var.RIGHT_HAND, var.BLUE)
            ot.output_text(img, "please extend your hand", var.FISRT_LANE, var.BLUE, var.SIZE_TXT_HINTS)
            # cv2.putText(img, "please extend your hand", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        else:
            color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
            if not up and int(angle_deg_DB) > 80 and int(angle_deg_DB) < 110:
                color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
                if points[16][1] < points[5][1] and points[14][1] < points[5][1]:
                    print("it's UP")
                    up = True
                    counter += 1
                    print(counter)
                    color.color_landmark(img, points, var.RIGHT_HAND, var.RED)
                    # voice.speak("it's UP, great, now bring it down slowly")
            elif up and points[16][1] > points[24][1] and points[14][1] > points[12][1]:
                print("its down")
                up = False
                color.color_landmark(img, points, var.RIGHT_HAND, var.RED)
                # voice.speak("go up fast")
                # voice.speak("it's down, great, now bring it up slowly")
        print("--------------")


    ot.output_text(img, str(counter), var.FISRT_LANE, var.RED, var.SIZE_TXT_HINTS)
    # cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
