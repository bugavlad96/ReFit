# in core voi avea o functie care preia toti parametrii corpului majoritatea reprezentand
# unghiurile a diferitor parti ale corpului cu verificarea vizibilitatii lor
# color landmark
from typing import Dict, Tuple

# des - means desired
# l - left
# r - right

import libs.utils as utils
import libs.global_var as var
import libs
# voi primi array-uri cu landmark-uri din global_var.py


def step(results, img, body_parts, body_angles, permissive_error):

    if len(body_parts) == 0:
        print("no body parts requested in this step")
        return None
    if len(body_angles) == 0:
        print("no body angles requested in this step")
        return None
    if len(body_parts) != len(body_angles):
        print("corresponding angles are missing for the requested body parts in the steps")
        print('len(body_parts): ', len(body_parts))
        print('len(body_angles): ', len(body_angles))

        return None


    actual_values = {}
    break_occurred = False
    for index, body_part_array in enumerate(body_parts):
        print("step_step: ", index, ' ', body_part_array)

        points = utils.collect_points(img, results)
        body_part_name = var.find_variable_name(body_part_array)

        if utils.are_points_visible(results, body_part_array):
            print(f"I can see your {body_part_name}")
            is_good, actual_angle = utils.is_body_angle_correct(body_part_array, body_angles[index], permissive_error, points)
            if is_good:
                print(f"good {body_part_name} angle")
                # actual_values += body_part_array, (True, actual_angle)
                actual_values[body_part_name] = (body_part_array, (True, actual_angle))
            else:
                print(f"Correct your {body_part_name} angle to {body_angles[index]}")
                actual_values[body_part_name] = (body_part_array, (False, actual_angle))
                break_occurred = True
                break
        else:
            print(f"I cannot see your {body_part_name} ")
            actual_values[body_part_name] = (body_part_array, (False, var.NOT_VALID))
            break_occurred = True
            break

    if not is_step_completed(actual_values):
        return var.STEP_NOT_COMPLETED, actual_values


    # the returned value is a dict: var.STEP_COMPLETED, (key = "LEFT_HAND", value = [var.LEFT_HAND, [False, 180grade]]), (bool:daca unghiul e in range-ul potrivit, valoarea unghiului)
    return var.STEP_COMPLETED, actual_values

def is_step_completed(actual_values):
    for body_part_txt, (body_part_array, angle) in actual_values.items():
        if not angle[0]:
            return False
        # print(angle[0])
        # print(angle[1])

    return True
    # if break_occured:
    #     return None
    # OR
    # if len(actual_angles) == len(body_angles):
    #     last_bool = list(actual_angle.keys())[-1]
    #     if not last_bool:
    #         return None
    # else:
    #     return None






#
# def step(results, img, permissive_error,
#          des_l_elbow=None, des_r_elbow=None,
#          des_l_shoulder=None, des_r_shoulder=None,
#          des_l_hip=None, des_r_hip=None,
#          des_l_knee=None, des_r_knee=None):
#          # des_l_ankle=None, des_r_ankle=None):
#
#     points = utils.collect_points(img, results)
#
#
#     if des_l_elbow and (des_l_elbow is not None):
#         #         check visibility
#         # check if the right angle
#         if utils.are_points_visible(results, var.LEFT_HAND):
#             print("I can see your LEFT ELBOW ")
#             if utils.is_body_angle_correct(var.LEFT_HAND, des_l_elbow, permissive_error, points):
#                 print("good left elbow angle")
#             else:
#                 print("Correct your LEFT ELBOW angle")
#         else:
#             print("I cannot see your LEFT ELBOW ")
#
#     if des_r_elbow and (des_r_elbow is not None):
#         #         check visibility
#         # check if the right angle
#         if utils.are_points_visible(results, var.RIGHT_HAND):
#             print("I can see your RIGHT ELBOW ")
#             if utils.is_body_angle_correct(var.RIGHT_HAND, des_r_elbow, permissive_error, points):
#                 print("GOOD RIGHT ELBOW angle")
#             else:
#                 print("Correct your RIGHT ELBOW angle")
#         else:
#             print("I cannot see your RIGHT ELBOW ")
#
#
#     if des_l_shoulder and (des_l_shoulder is not None):
#         #         check visibility
#         # check if the right angle
#         if utils.are_points_visible(results, var.LEFT_SHOULDER):
#             print("I can see your LEFT SHOULDER")
#             if utils.is_body_angle_correct(var.LEFT_SHOULDER, des_l_shoulder, permissive_error, points):
#                 print("GOOD LEFT SHOULDER  angle")
#             else:
#                 print("Correct your LEFT SHOULDER  angle")
#         else:
#             print("I cannot see your LEFT SHOULDER")
#
#
#     if des_r_shoulder and (des_r_shoulder is not None):
#         #         check visibility
#         # check if the right angle
#         if not utils.are_points_visible(results, var.RIGHT_SHOULDER):
#             print("I can see your RIGHT SHOULDER ")
#             if utils.is_body_angle_correct(var.RIGHT_SHOULDER, des_r_shoulder, permissive_error, points):
#                 print("GOOD RIGHT SHOULDER angle")
#             else:
#                 print("Correct your RIGHT SHOULDER angle")
#         else:
#             print("I cannot see your RIGHT SHOULDER ")
#
#
#
#     if des_l_hip and (des_l_hip is not None):
#         #         check visibility
#         # check if the right angle
#         if  utils.are_points_visible(results, var.LEFT_HIP):
#             print("I can see your LEFT HIP")
#             if  utils.is_body_angle_correct(var.LEFT_HIP, des_l_hip, permissive_error, points):
#                 print("GOOD your LEFT HIP angle")
#             else:
#                 print("Correct your LEFT HIP angle")
#
#         else:
#             print("I cannot see your LEFT HIP")
#
#     if des_r_hip and (des_r_hip is not None):
#             #         check visibility
#             # check if the right angle
#             if utils.are_points_visible(results, var.RIGHT_HIP):
#                 print("I can see your RIGHT HIP ")
#                 if  utils.is_body_angle_correct(var.RIGHT_HIP, des_r_hip, permissive_error, points):
#                     print("GOOD RIGHT HIP angle")
#                 else:
#                     print("Correct your RIGHT HIP angle")
#
#             else:
#                 print("I cannot see your RIGHT HIP ")
#
#     if des_l_knee and (des_l_knee is not None):
#             #         check visibility
#             # check if the right angle
#             if  utils.are_points_visible(results, var.LEFT_FOOT):
#                 print("I can see your LEFT KNEE")
#                 if utils.is_body_angle_correct(var.LEFT_FOOT, des_l_knee, permissive_error, points):
#                     print("GOOD LEFT KNEE angle")
#                 else:
#                     print("Correct your LEFT KNEE angle")
#
#             else:
#                 print("I cannot see your LEFT KNEE")
#
#     if des_r_knee and (des_r_knee is not None):
#             #         check visibility
#             # check if the right angle
#             if utils.are_points_visible(results, var.RIGHT_FOOT):
#                 print("I can see your RIGHT KNEE ")
#                 if utils.is_body_angle_correct(var.RIGHT_FOOT, des_r_knee, permissive_error, points):
#                     print("GOOD RIGHT KNEE angle")
#                 else:
#                     print("Correct your RIGHT KNEE angle")
#
#             else:
#                 print("I cannot see your RIGHT KNEE ")
#
#     # daca-s avea un array de body parts pe care le voi primi, le pot verifica cu find_variable_name
#     # si sa generalizez metoda!!!!!!!!!!!!!!!!!!!!!!!!
#
