import libs.global_var as var
import libs.visible_landmark as vl
import body_orientation as body_exp
import libs.global_var as var
import body_orientation as bo

def body_snap_position_exersize(results, img, desired_body_orientation, desired_body_postion, desired_knee_angle = None, desired_hip_angle = None, desired_shoulder_angle = None, desired_elbow_angle = None):

    # Daca se vad toate punctele in dependenta de orientare mai putin de la glezna un jos?

    if bo.body_orientation(desired_body_orientation, results, img):
        print(f"Body orientation {var.find_variable_name(desired_body_orientation)} is GOOD")
        if vl.are_points_visible(results, desired_body_postion):
            print(f"Body position {var.find_variable_name(desired_body_postion)} is GOOD")
        else:
            print(f"Body orientation {var.find_variable_name(desired_body_postion)} is BAD")
    else:
        print(f"Body orientation {var.find_variable_name(desired_body_orientation)} is BAD")

        # Conteaza si orientarea

        body_exp.body_orientation()
        # if staut in pcioare


        # if stau asezat


        # is stau culca
        #     culcat complet sau sustinut pe maini

        if vl.are_points_visible(results, desired_body_orientation):
            return print("BODY orientation - GOOD")
        else:
            print("BODY orientation - BAD")