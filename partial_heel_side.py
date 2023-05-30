# https://youtu.be/ZTnYVDn7RD4?t=92
import threading

import mediapipe as mp
import cv2
import numpy as np
# import pyttsx3
import tests.voice_tests.voice as voice
import math
import libs.visible as visible
import threading

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

        # 23 - left hip         # 23 - șold stâng
        # 24 - right hip        # 24 - șold drept
        # 25 - left knee        # 25 - genunchiul stâng
        # 26 - right knee       # 26 - genunchiul drept
        # 27 - left ankle       # 27 - glezna stângă
        # 28 - right ankle      # 28 - glezna dreaptă
        # 29 - left heel        # 29 - călcâiul stâng
        # 30 - right heel       # 30 - călcâiul drept
        # 31 - left foot index  # 31 - indicele piciorului stâng
        # 32 - right foot index # 32 - indicele piciorului drept

        #left leg
        vector_AB = (points[23][0] - points[25][0], points[23][1] - points[25][1])
        vector_BC = (points[25][0] - points[27][0], points[25][1] - points[27][1])
        #right leg
        vector_EF = (points[24][0] - points[26][0], points[24][1] - points[26][1])
        vector_FG = (points[26][0] - points[28][0], points[26][1] - points[28][1])
        # Calculate the dot product of AB and BC, rezulta un scalar
        dot_product_AC = vector_AB[0] * vector_BC[0] + vector_AB[1] * vector_BC[1]
        dot_product_EG = vector_EF[0] * vector_FG[0] + vector_EF[1] * vector_FG[1]

        # Calculate the magnitudes of AB and BC
        magnitude_AB = math.sqrt(vector_AB[0] ** 2 + vector_AB[1] ** 2)
        magnitude_BC = math.sqrt(vector_BC[0] ** 2 + vector_BC[1] ** 2)
        magnitude_EF = math.sqrt(vector_EF[0] ** 2 + vector_EF[1] ** 2)
        magnitude_FG = math.sqrt(vector_FG[0] ** 2 + vector_FG[1] ** 2)

        # Calculate the cosine of the angle between AB and BC
        cosine_angle_AC = dot_product_AC / (magnitude_AB * magnitude_BC)
        cosine_angle_EG = dot_product_EG / (magnitude_EF * magnitude_FG)

        # Calculate the angle in radians
        angle_rad_AC = math.acos(cosine_angle_AC)
        angle_rad_EG = math.acos(cosine_angle_EG)

        # Convert the angle to degrees
        angle_deg_AC = abs(math.degrees(angle_rad_AC) - 180)
        angle_deg_EG = abs(math.degrees(angle_rad_EG) - 180)



        cv2.putText(img, str(int(angle_deg_AC)), (points[25][0], points[25][1]), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)
        cv2.putText(img, str(int(angle_deg_EG)), (points[26][0], points[26][1]), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

        # print("Angle (degrees):", angle_deg_AC)

        if (int(angle_deg_AC) >= 165 and int(angle_deg_EG) >= 165) and (counter_left == counter_right == 0):
            cv2.circle(img, points[23], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[25], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[27], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[24], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[26], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[28], 15, (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "Great, now, begin the exercise :), bring a knee at a time ", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        elif counter_left != 0 or counter_right != 0:
            # if int(angle_deg_AC) >= 165 and int(angle_deg_EG) >= 165:
            #     cv2.circle(img, points[23], 15, (0, 255, 0), cv2.FILLED)
            #     cv2.circle(img, points[25], 15, (0, 255, 0), cv2.FILLED)
            #     cv2.circle(img, points[27], 15, (0, 255, 0), cv2.FILLED)
            #     cv2.circle(img, points[24], 15, (0, 255, 0), cv2.FILLED)
            #     cv2.circle(img, points[26], 15, (0, 255, 0), cv2.FILLED)
            #     cv2.circle(img, points[28], 15, (0, 255, 0), cv2.FILLED)
            #     cv2.putText(img, str("good job, now go up again...."), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0),
            #                 2)
            #     left_up = False
            #     right_up = False
            if int(angle_deg_AC) >= 165 and int(angle_deg_EG) < 165:
                cv2.circle(img, points[23], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[25], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[27], 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str("good job, LEFT is down. Now bring the left leg up...."), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2,
                            (0, 255, 0),
                            2)
                left_up = False
            if int(angle_deg_AC) < 165 and int(angle_deg_EG) >= 165:
                cv2.circle(img, points[23], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[25], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[27], 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str("good job, RIGHT is down. Now bring the right leg up...."), (100, 200), cv2.FONT_HERSHEY_PLAIN, 2,
                            (0, 255, 0),
                            2)
                right_up = False
        if not(left_up) and (int(angle_deg_AC) < 165):
            cv2.circle(img, points[23], 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, points[25], 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, points[27], 15, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "a little more with your left", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            if int(angle_deg_AC) < 65:
                left_up = True
                counter_left += 1
                # print(counter)
                # voice.speak("it's UP, great, now bring it down slowly")
                cv2.circle(img, points[23], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[25], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[27], 15, (255, 0, 0), cv2.FILLED)
                cv2.putText(img, str("great, LEFT is up. Now go down slowly in a controlled way, extend fully your foot"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        if not(right_up) and (int(angle_deg_EG) < 165):
            cv2.circle(img, points[24], 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, points[26], 15, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, points[28], 15, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "a little more with your right", (150, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            if int(angle_deg_EG) < 65:
                right_up = True
                counter_right += 1
                # print(counter)
                # voice.speak("it's UP, great, now bring it down slowly")
                cv2.circle(img, points[24], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[26], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[28], 15, (255, 0, 0), cv2.FILLED)
                cv2.putText(img,
                            str("great, RIGHT is up. Now go down slowly in a controlled way, extend fully your foot"),
                            (100, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        if left_up:
            if int(angle_deg_AC) < 65:
                cv2.circle(img, points[23], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[25], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[27], 15, (255, 0, 0), cv2.FILLED)
                cv2.putText(img, str("great, LEFT is up. Now go down slowly in a controlled way, extend fully your foot"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            elif int(angle_deg_AC) > 65 and int(angle_deg_AC) <= 165:
                cv2.circle(img, points[23], 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, points[25], 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, points[27], 15, (0, 0, 255), cv2.FILLED)
                cv2.putText(img, str("try to bring SLOWLY your LEFT knee as close as possible to the ground..."), (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        if right_up:
            if int(angle_deg_EG) < 65:
                cv2.circle(img, points[24], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[26], 15, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, points[28], 15, (255, 0, 0), cv2.FILLED)
                cv2.putText(img,str("great, RIGHT is up. Now go down slowly in a controlled way, extend fully your foot"), (100, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            elif int(angle_deg_EG) > 65 and int(angle_deg_EG) <= 165:
                cv2.circle(img, points[24], 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, points[26], 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, points[28], 15, (0, 0, 255), cv2.FILLED)
                cv2.putText(img, str("try to bring SLOWLY your RIGHT knee as close as possible to the ground..."), (150, 200), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        print("--------------")



    cv2.putText(img, str(counter_left), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)
    cv2.putText(img, str(counter_right), (300, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)


    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
