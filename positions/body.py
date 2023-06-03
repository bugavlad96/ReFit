import libs.global_var as var
import libs.visible_landmark as vl

def body(desired_body_orientation, results, img):

    if vl.are_points_visible(results, desired_body_orientation):
        return print("BODY orientation - GOOD")
    else:
        print("BODY orientation - BAD")