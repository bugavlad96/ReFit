import core.step as steps
import libs.global_var as var
import libs.utils as utils
import libs.prepare_stream_BGR2RGB as ps
import core.step as step
import mediapipe as mp
import cv2
import libs.color_landmark as color
import libs.output_text
import libs.output_text as ot



# trebuie sa vad cum implementez functia de counter pentru a masura succesul
# IDEE: la desenat poate merge sa desenezi sageti care sa indice directia de miscare pe stream


# trebuie de implementat counter, oare n-ar fie o idee de a pune in pasul de steps
# O lista de dictionare

            # body_parts, steps(va contine o succesiune de unghiuri) persmissive_error
def exercise(body_parts, steps_angles, permissive_error, count_max):
    # TREBUIE DE BAGAT TOT WHILE TRUE-ul pentru ca sa se execute aici!!!!!!!!!!!!!!!!!!

    # --------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------

    # initialize some vars
    up = False

    counter = 0
    are_steps_completed = []
    actual_values = []

    first_half_exercise = False
    second_half_exercise = False

    # for idx in range(len(body_parts)):
    #     are_steps_completed[idx] = var.STEP_NOT_COMPLETED
    are_steps_completed =[False for _ in range(len(steps_angles))]
    actual_values = [-1 for _ in range(len(steps_angles))]

    mpDraw, mpPose, pose, cap = utils.exercise_initialization()


    while True:

        img, results = ps.prepare_stream(cap, pose)

        # the condition will be True if at least one pose landmark is detected.
        # aici poti verifica daca faci displaty doar la landmark-urile relevante sau le lasi pe toate
        if results.pose_landmarks:
            # printeaza punctele si conexiunile. Oferit de mdedia pipe
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            points = utils.collect_points(img, results)

            if not first_half_exercise:
                print("am intrat")
                for idx, is_step_completed in enumerate(are_steps_completed):

                    if (not is_step_completed):
                        # print(idx, is_step_completed)
                        print(f"index {idx}")
                        are_steps_completed[idx], actual_values[idx] = step.step(results, img, body_parts, steps_angles[idx], permissive_error)
                        if not are_steps_completed[idx]:
                            print(f"{idx} NOT completed")
                            break
                        else:
                            print(f"{idx}  SUCCESS")
                            if idx == len(are_steps_completed) - 1:
                                print("the last step up")
                                first_half_exercise = True

                                print(counter)
                                are_steps_completed = [False for _ in range(len(steps_angles))]


            if first_half_exercise:
                print("in intrat in sens invers")

                for idx, is_step_completed in reversed(list(enumerate(are_steps_completed))):
                    if (not is_step_completed):
                        are_steps_completed[idx], actual_values[idx] = step.step(results, img, body_parts, steps_angles[idx], permissive_error)
                        if not are_steps_completed[idx]:
                            print(f"{idx} NOT completed")
                            break
                        else:
                            print(f"{idx}  SUCCESS")
                            if idx == 0:
                                print("the last step dowm")
                                counter += 1
                                first_half_exercise = False
                                # second_half_exercise = True
                                are_steps_completed = [False for _ in range(len(steps_angles))]


            if counter == count_max:
                break

            print("--------------")


        ot.output_text(img, str(counter), var.FISRT_LANE, var.RED, var.SIZE_TXT_HINTS)
        # cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)

        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return counter

















    # --------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------


    # # ARRAY DE COUNTERI daca e counter separat pentru fiecare parte a copului
    # # un array de pasi
    #
    # # initialize the step complition
    # is_step_completed = []
    #
    # for idx in range(len(list_of_steps)):
    #     is_step_completed[idx-1] = var.STEP_NOT_COMPLETED
    #
    #
    # # in list_of_steps ordinea conteaza
    # # gandeste-te la inversarea executarii pasilor
    # # if fac prima jumatate revin sa fac in ordine inversa
    # for step in list_of_steps:
    #     if is_step_completed[]
    #
    #
    #
    # return succes, counter_list