RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
# for text output on live stream
FISRT_LANE = (50, 150)
FISRT_LANE_SECOND_COUNTER = (300, 150)
SECOND_LANE = (50, 200)
# Stream size ouput
STREAM_RESIZE = (1280, 960)

# text size on stream
SIZE_TXT_HINTS = 2
SIZE_ANGLES = 2

# For angle computation
RIGHT_ELBOW = [12, 14, 16]
LEFT_ELBOW = [11, 13, 15]
# left_shoulder -> right_shouler -> right elbow
RIGHT_SHOULDER = [11, 12, 14]
# right shoulder -> left_shoulder -> left Elbow
LEFT_SHOULDER = [12, 11, 13]

#hips to compute the angles
LEFT_HIP = [11, 23, 25]
RIGHT_HIP = [12, 24, 26]
# feet
LEFT_KNEE = [23, 25, 27]
RIGHT_KNEE = [24, 26, 28]

NOT_VISIBLE = False
VISIBLE     = True
NOT_VALID = -1

ANGLE_0   = 0
ANGLE_30  = 30
ANGLE_45  = 45
ANGLE_90  = 90
ANGLE_100 = 100
ANGLE_110 = 110
ANGLE_120 = 120
ANGLE_130 = 130
ANGLE_140 = 140
ANGLE_150 = 150
ANGLE_160 = 160
ANGLE_170 = 170
ANGLE_180 = 180

# admissible error deviatio
ERROR_10 = 10
ERROR_15 = 15
ERROR_20 = 20
ERROR_25 = 25

# Body orientation
UPPER_FRONT = [23, 24, 11, 12, 0, 2, 5]
# from hips till ankles
LOWER_FRONT = [23, 24, 25, 26, 27, 28]
# EXPOSED_LEFT
UPPER_LEFT_SIDE = [11, 13, 15, 7]
# EXPOSED_RIGHT
UPPER_RIGHT_SIDE = [12, 14, 16, 8]

STEP_COMPLETED = True
STEP_NOT_COMPLETED =False


# # Body position
# BODY_POSITION_STAND_STILL = []
# BODY_POSITION_SEATED_STILL = 1010
# BODY_POSITION_LAYING_STILL = 1020
# BODY_POSITION_LAYING_BENDED = 1021


# method to look for variable global var name based on the value
def find_variable_name(value):
    for name, val in globals().items():
        if val == value:
            return name
    return None

def find_variable_value(req_name):
    for name, val in globals().items():
        if req_name == name:
            return val
    return None
