# https://www.youtube.com/watch?v=432yWPJQ-is  min:5:29
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
up = False
counter = 0

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

        # testing here
        # vector_AB = umar cot
        # vector_BC = cot incheietura
        # vector_DA = (points[11][0] - points[12][0], points[11][1] - points[12][1])
        vector_AB = (points[12][0] - points[14][0], points[12][1] - points[14][1])
        vector_BC = (points[14][0] - points[16][0], points[14][1] - points[16][1])


        # Calculate the dot product of AB and BC, rezulta un scalar
        # dot_product_DB = vector_DA[0] * vector_AB[0] + vector_DA[1] * vector_AB[1]
        dot_product_AC = vector_AB[0] * vector_BC[0] + vector_AB[1] * vector_BC[1]

        # Calculate the magnitudes of AB and BC
        # magnitude_DA = math.sqrt(vector_DA[0] ** 2 + vector_DA[1] ** 2)
        magnitude_AB = math.sqrt(vector_AB[0] ** 2 + vector_AB[1] ** 2)
        magnitude_BC = math.sqrt(vector_BC[0] ** 2 + vector_BC[1] ** 2)

        # Calculate the cosine of the angle between AB and BC
        # cosine_angle_DB = dot_product_DB / (magnitude_DA * magnitude_AB)
        cosine_angle_AC = dot_product_AC / (magnitude_AB * magnitude_BC)

        # Calculate the angle in radians
        # angle_rad_DB = math.acos(cosine_angle_DB)
        angle_rad_AC = math.acos(cosine_angle_AC)

        # Convert the angle to degrees
        # angle_deg_DB = math.degrees(angle_rad_DB)
        angle_deg_AC = math.degrees(angle_rad_AC)



        cv2.putText(img, str(int(angle_deg_AC)), (points[14][0], points[14][1]), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)
        # cv2.putText(img, str(int(angle_deg_DB)), (points[12][0], points[12][1]), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # print("Angle (degrees):", angle_deg_AC)


        if int(angle_deg_AC) >= 0 and int(angle_deg_AC) <= 10 and points[20][1] > points[24][1] and counter == 0:
            cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
            cv2.putText(img, "YOU CAN START THE EXERCISE", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        elif not up:
            if int(angle_deg_AC) >= 0 and int(angle_deg_AC) <= 10 and points[20][1] > points[24][1] and counter > 0:
                cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str("great, it's down, now bring it up slowly"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            elif (int(angle_deg_AC) >= 10 and int(angle_deg_AC) <= 80) or (int(angle_deg_AC) >= 100):
                cv2.circle(img, points[12], 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, points[14], 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, points[16], 15, (0, 0, 255), cv2.FILLED)
                cv2.putText(img, str("elbow angle must be ~90 deg"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255),
                            2)
            if points[14][1] > points[12][1] and  int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:
                cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str("~90 angle, good to go"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            elif points[16][1] < points[12][1] and abs(points[14][1] - points[12][1]) <= 50 and int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:
                up = True
                counter += 1
                print(counter)
                # voice.speak("it's UP, great, now bring it down slowly")
                cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str("great, it's up"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        elif up:
            if points[16][1]+30 < points[14][1] and int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:
            # if points[16][1] < points[12][1] and abs(points[14][1] - points[12][1]) <= 50 and int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:

            # if (points[14][1] + 20)  < points[12][1] and  int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:
                cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str("go down slowly"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            elif points[16][1]+30 < points[14][1] and ((int(angle_deg_AC) >= 10 and int(angle_deg_AC) <= 80) or (int(angle_deg_AC) >= 100)):
            # elif points[16][1]+30 < points[14][1] and int(angle_deg_AC) >= 100 and int(angle_deg_AC) <= 80:
                cv2.circle(img, points[12], 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, points[14], 15, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, points[16], 15, (0, 0, 255), cv2.FILLED)
                cv2.putText(img, str("elbow angle must be ~90 deg"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

            if abs(points[14][1] - points[16][1]) <= 30 and int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:
                    cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, str("great, now extend the hand"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    extended = True

            elif points[16][1]+30 >= points[14][1] and int(angle_deg_AC) < 80 and extended:
                cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
                cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
                if int(angle_deg_AC) >= 0 and int(angle_deg_AC) <= 10 and points[20][1] > points[24][1]:
                    print("its down")
                    up = False
                    extended = False
                    # # voice.speak("go up fast")
                    # # voice.speak("it's down, great, now bring it up slowly")
                    cv2.circle(img, points[12], 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, points[14], 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(img, points[16], 15, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, str("great, it's down, now bring it up slowly"), (100, 150),
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            # elif int(angle_deg_AC) < 80 and not(extended):
            #     cv2.circle(img, points[12], 15, (0, 0, 255), cv2.FILLED)
            #     cv2.circle(img, points[14], 15, (0, 0, 255), cv2.FILLED)
            #     cv2.circle(img, points[16], 15, (0, 0, 255), cv2.FILLED)
            #     cv2.putText(img, str("get back to top position, and  ~90deg"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)



            # elif abs(points[14][1] - points[16][1]) <= 50 and int(angle_deg_AC) <= 100 and int(angle_deg_AC) >= 80:
            #     cv2.circle(img, points[12], 15, (0, 0, 255), cv2.FILLED)
            #     cv2.circle(img, points[14], 15, (0, 0, 255), cv2.FILLED)
            #     cv2.circle(img, points[16], 15, (0, 0, 255), cv2.FILLED)

                # cv2.putText(img, str("elbow angle must be ~90 deg"), (100, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


        print("--------------")



    cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
