# where exercise will be called
import core.exercise as ex
import libs.global_var as var

body_parts = [var.LEFT_ELBOW, var.RIGHT_ELBOW, var.LEFT_SHOULDER, var.RIGHT_SHOULDER]

body_angles_step1 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_110, var.ANGLE_110]
body_angles_step2 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_140, var.ANGLE_140]
body_angles_step3 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_160, var.ANGLE_160]
body_angles_step4 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_180, var.ANGLE_180]

steps = [[var.ANGLE_170, var.ANGLE_170, var.ANGLE_110, var.ANGLE_110],
         [var.ANGLE_170, var.ANGLE_170, var.ANGLE_140, var.ANGLE_140],
         [var.ANGLE_170, var.ANGLE_170, var.ANGLE_160, var.ANGLE_160],
         [var.ANGLE_170, var.ANGLE_170, var.ANGLE_180, var.ANGLE_180]]

print(ex.exercise(body_parts, steps, var.ERROR_10))