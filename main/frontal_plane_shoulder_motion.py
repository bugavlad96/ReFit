# https://www.youtube.com/watch?v=_GoXq9H0hqg

import mediapipe as mp
import cv2
import libs.color_landmark as color
import libs.output_text
import libs.output_text as ot
import libs.global_var as var
import libs.prepare_stream_BGR2RGB as ps
import libs.utils as utils
import core.step as step


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

is_completed_step1 = False
is_completed_step2 = False
is_completed_step3 = False
is_completed_step4 = False

actual_values = {}


while True:

    img, results = ps.prepare_stream(cap, pose)

    # the condition will be True if at least one pose landmark is detected.
    # aici poti verifica daca faci displaty doar la landmark-urile relevante sau le lasi pe toate
    if results.pose_landmarks:
        # printeaza punctele si conexiunile. Oferit de mdedia pipe
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        points = utils.collect_points(img, results)

        # Test new functions
        # print(foot.left_foot(180, 10, results, img, 180))
        # print(foot.right_foot(180, 10, results, img, 180))
        # print(body.body(var.EXPOSED_UPPER_FRONT, results, img))
        # print(hand.left_hand(90, 10, results, img, 180))
        # print(hand.right_hand(90, 10, results, img, 180))
        # print(bpa.body_part_angle(var.RIGHT_HAND, 90, 10, points))
        # end test


        # compute the angles
        # angle_deg_AC = ca.compute_angle(points, var.RIGHT_HAND)
        # ot.output_angle(img, points, var.RIGHT_HAND[1], angle_deg_AC, var.RED)
        #
        # angle_deg_DB = ca.compute_angle(points, var.RIGHT_SHOULDER)
        # ot.output_angle(img, points, var.LEFT_SHOULDER[1], angle_deg_DB, var.RED)



# !!!!!!!!!o idee: daca stepul presupune o crestere de unghi atunci mareste ca regula cu Eroarea admisibila + 10 grade?
#         body_parts =[var.LEFT_ELBOW, var.RIGHT_ELBOW]#, var.LEFT_SHOULDER, var.RIGHT_SHOULDER]
#         # body_angles = [var.ANGLE_90, var.ANGLE_90, var.ANGLE_180, var.ANGLE_180]
#         # step.step(results, img, body_parts, body_angles, var.ERROR_10)
#         # body_parts_step1 =
#         body_angles_step1 = [var.ANGLE_30, var.ANGLE_30]#, var.ANGLE_110, var.ANGLE_110]
#         # body_parts_step2
#         body_angles_step2 = [var.ANGLE_45, var.ANGLE_45]#, var.ANGLE_140, var.ANGLE_140]
#         # body_parts_step3
#         body_angles_step3 = [var.ANGLE_90, var.ANGLE_90]#, var.ANGLE_160, var.ANGLE_160]
#         # body_parts_step4
#         body_angles_step4 = [var.ANGLE_180, var.ANGLE_180]#, var.ANGLE_180, var.ANGLE_180]

        body_parts =[var.LEFT_ELBOW, var.RIGHT_ELBOW, var.LEFT_SHOULDER, var.RIGHT_SHOULDER]
        # body_angles = [var.ANGLE_90, var.ANGLE_90, var.ANGLE_180, var.ANGLE_180]
        # step.step(results, img, body_parts, body_angles, var.ERROR_10)
        # body_parts_step1 =
        body_angles_step1 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_110, var.ANGLE_110]
        body_angles_step2 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_140, var.ANGLE_140]
        body_angles_step3 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_160, var.ANGLE_160]
        body_angles_step4 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_180, var.ANGLE_180]
        # collor the landmarks in blue
        if not is_completed_step1:
            is_completed_step1, actual_values = step.step(results, img, body_parts, body_angles_step1, var.ERROR_10)
            libs.output_text.output_angles(img, points, actual_values, var.GREEN)
            print("great step1 completed")
        elif is_completed_step1:
            libs.output_text.output_angles(img, points, actual_values, var.BLUE)
            print("great step1 completed")

            if not is_completed_step2:
                is_completed_step2, actual_values = step.step(results, img, body_parts, body_angles_step2,var.ERROR_10)
                libs.output_text.output_angles(img, points, actual_values, var.GREEN)
                print("great step2 completed")
            elif is_completed_step2:
                libs.output_text.output_angles(img, points, actual_values, var.BLUE)
                print("great step2 completed")

                if not is_completed_step3:
                    is_completed_step3, actual_values = step.step(results, img, body_parts, body_angles_step3, var.ERROR_10)
                    libs.output_text.output_angles(img, points, actual_values, var.GREEN)
                    print("great step3 completed")
                elif is_completed_step3:
                    libs.output_text.output_angles(img, points, actual_values, var.BLUE)
                    print("great step3 completed")
                    if not is_completed_step4:
                        print("great step4 completed")
                        is_completed_step4, actual_values = step.step(results, img, body_parts, body_angles_step4, var.ERROR_10)
                        libs.output_text.output_angles(img, points, actual_values, var.GREEN)
                    elif is_completed_step4:
                        print("great step4 completed")
                        libs.output_text.output_angles(img, points, actual_values, var.BLUE)
                        counter += 1
                        is_completed_step1 = False
                        is_completed_step2 = False
                        is_completed_step3 = False
                        is_completed_step4 = False









            # ------------------------------stop here
            # if int(angle_deg_AC) >= 170 and points[20][1] > points[24][1] and counter == 0:
            #     color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
            #     ot.output_text(img, "YOU CAN START THE EXERCISE", var.FISRT_LANE, var.GREEN, var.SIZE_TXT_HINTS)
            #     # cv2.putText(img, "YOU CAN START THE EXERCISE", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            # elif int(angle_deg_AC) < 170:
            #     color.color_landmark(img, points, var.RIGHT_HAND, var.RED)
            #     ot.output_text(img, "please extend your hand", var.FISRT_LANE, var.BLUE, var.SIZE_TXT_HINTS)
            #     # cv2.putText(img, "please extend your hand", (150, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
            # else:
            #     color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
            #     if not up and int(angle_deg_DB) > 80 and int(angle_deg_DB) < 110:
            #         color.color_landmark(img, points, var.RIGHT_HAND, var.GREEN)
            #         if points[16][1] < points[5][1] and points[14][1] < points[5][1]:
            #             print("it's UP")
            #             up = True
            #             counter += 1
            #             print(counter)
            #             color.color_landmark(img, points, var.RIGHT_HAND, var.RED)
            #             # voice.speak("it's UP, great, now bring it down slowly")
            #     elif up and points[16][1] > points[24][1] and points[14][1] > points[12][1]:
            #         print("its down")
            #         up = False
            #         color.color_landmark(img, points, var.RIGHT_HAND, var.RED)
            #         # voice.speak("go up fast")
            #         # voice.speak("it's down, great, now bring it up slowly")
        print("--------------")


    ot.output_text(img, str(counter), var.FISRT_LANE, var.RED, var.SIZE_TXT_HINTS)
    # cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
