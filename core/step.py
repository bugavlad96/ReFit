# in core voi avea o functie care preia toti parametrii corpului majoritatea reprezentand
# unghiurile a diferitor parti ale corpului cu verificarea vizibilitatii lor
# color landmark
from typing import Dict, Tuple

# des - means desired
# l - left
# r - right

import libs.utils as utils
import libs.global_var as var

# voi primi array-uri cu landmark-uri din global_var.py


def step_experiment(results, img, body_parts, body_angles, permissive_error):

    if len(body_parts) == 0:
        return print("no body parts requested in this step")
    if len(body_angles) == 0:
        return print("no body angles requested in this step")
    if len(body_parts) != len(body_angles):
        return print(" corresponding angles are missing for the requested body parts in the steps")

    for index, body_part_value in enumerate(body_parts):

        points = utils.collect_points(img, results)
        body_part_name = var.find_variable_name(body_part_value)

        if utils.are_points_visible(results, body_part_value):
            print(f"I can see your {body_part_name}")

            if utils.is_body_angle_correct(body_part_value, body_angles[index], permissive_error, points):
                print(f"good {body_part_name} angle")
            else:
                print(f"Correct your {body_part_name} angle")
        else:
            print(f"I cannot see your {body_part_name} ")


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
