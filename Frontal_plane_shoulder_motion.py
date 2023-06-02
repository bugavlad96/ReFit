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

    # the condition will be True if at least one pose landmark is detected.
    # aici poti verifica daca faci displaty doar la landmark-urile relevante sau le lasi pe toate
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
        if int(angle_deg_AC) >= 0 and int(angle_deg_AC) <= 10 and points[20][1] > points[24][1] and counter == 0:
            # poitns_right_hand
            color_this_points = [12, 14, 16]
            color_code = [0, 255, 0]
            color.color_landmark(img, points, color_this_points, color_code)
            # cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
            # cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
            # cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "YOU CAN START THE EXERCISE", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        elif int(angle_deg_AC) > 10:
            cv2.circle(img, points[12], 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, points[14], 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, points[16], 15, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "please extend your hand", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        else:
            cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
            if not up and int(angle_deg_DB) > 60 and int(angle_deg_DB) < 80:
                cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
                if points[16][1] < points[5][1] and points[14][1] < points[5][1]:
                    print("it's UP")
                    up = True
                    counter += 1
                    print(counter)
                    # voice.speak("it's UP, great, now bring it down slowly")
                    cv2.circle(img, points[12], 15, (255, 0, 0), cv2.FILLED)
                    cv2.circle(img, points[14], 15, (255, 0, 0), cv2.FILLED)
                    cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)
            elif up and points[16][1] > points[24][1] and points[14][1] > points[12][1]:
                print("its down")
                up = False
                # voice.speak("go up fast")
                # voice.speak("it's down, great, now bring it up slowly")
                cv2.circle(img, points[12], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[14], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[16], 15, (255, 0, 0), cv2.FILLED)
        print("--------------")



    cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
