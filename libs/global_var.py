

RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
# 12 - right shoulder
# 14 - right elbow
# 16 - right wrist
RIGHT_HAND = [12, 14, 16]
LEFT_HAND = [11, 13, 15]
# left_shoulder -> right_shouler -> right elbow
RIGHT_SHOULDER = [11, 12, 14]
# right shoulder -> left_shoulder -> left Elbow
LEFT_SHOULDER = [12, 11, 13]

# for text output
FISRT_LANE = (50, 150)
FISRT_LANE_SECOND_COUTER = (300, 150)
SECOND_LANE = (50, 200)

STREAM_RESIZE = (1280, 960)

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
LEFT_FOOT = [23, 25, 27]
RIGHT_FOOT = [24, 26, 28]

SIZE_TXT_HINTS = 2
SIZE_TXT_KEY = 12

# Body orientation
# EXPOSED_FRONT = "exposed_front"
# EXPOSED_LEFT  = "exposed_right"
# EXPOSED_RIGHT = "exposed_RIGHT"
# Body orientation
EXPOSED_UPPER_FRONT = [23, 24, 11, 12, 15, 16, 0, 2, 5]
# from hips till ankles
EXPOSED_LOWER_FRONT = [23, 24, 25, 26, 27, 28]
EXPOSED_LEFT  = [11, 13, 15, 7]
EXPOSED_RIGHT = [12, 14, 16, 8]
LEFT_HIP = [11, 23, 25]
RIGHT_HIP = [12, 24, 26]
NOT_VISIBLE = False
VISIBLE     = True