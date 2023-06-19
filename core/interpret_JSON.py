# where exercise will be called
# import core.exercise as ex
import libs.global_var as var
import json
import core.exercise as ex
#
# # body_angles_step1 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_110, var.ANGLE_110]
# # body_angles_step2 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_140, var.ANGLE_140]
# # body_angles_step3 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_160, var.ANGLE_160]
# # body_angles_step4 = [var.ANGLE_170, var.ANGLE_170, var.ANGLE_180, var.ANGLE_180]
#
# body_parts = [var.LEFT_ELBOW, var.RIGHT_ELBOW, var.LEFT_SHOULDER, var.RIGHT_SHOULDER]
# steps = [[var.ANGLE_170, var.ANGLE_170, var.ANGLE_110, var.ANGLE_110],
#          [var.ANGLE_170, var.ANGLE_170, var.ANGLE_140, var.ANGLE_140],
#          [var.ANGLE_170, var.ANGLE_170, var.ANGLE_160, var.ANGLE_160],
#          [var.ANGLE_170, var.ANGLE_170, var.ANGLE_180, var.ANGLE_180]]
#
# print(ex.exercise(body_parts, steps, var.ERROR_10, 4))

json_data = '''{
  "Name": "Exercise Hand",
  "Count_max": 4,
  "Permissive_error": 10,
  "Steps": {
            "step_0": {
              "RIGHT_ELBOW": 90,
              "LEFT_ELBOW": 90
            },
            "step_1": {
              "RIGHT_ELBOW": 180,
              "LEFT_ELBOW": 180
            },
            "step_2": {
              "RIGHT_ELBOW": 200,
              "LEFT_ELBOW": 200
            }
  }
}'''

def interpret_json(json_data):
    body_parts = []
    steps_angles = []
    nr_body_parts = 0
    data = json.loads(json_data)

    name = data["Name"]
    print(name)
    count_max = data["Count_max"]
    permissive_error = data["Permissive_error"]

    steps = data["Steps"]
    for step_key, step_value in steps.items():
        print("Step:", step_key)
        print('step_value: ', step_value)
        step_angles = []
        for body_part, angle in step_value.items():
            # nr_body_parts = len(step_value)
            # presupunerea e ca la fiecare pas am aceleasi parti ale corpului (partea 1,2 si 3 an aceeasi ordime) pentru totii pasii. tot ce se schimba la pasii ulteriori sunt unghiurile
            if len(body_parts) < len(step_value):
                print('len(body_parts): ', len(body_parts))
                print('len(step_value): ', len(step_value))
                print("body_parts: ", body_parts)
                print('step_value: ', step_value)
                value = var.find_variable_value(body_part)
                if value is None:
                    return print("No such body_part")

                body_parts.append(value)
                step_angles.append(angle)
            else:
                step_angles.append(angle)

        steps_angles.append(step_angles)

    print("din functia json: ", body_parts)
    print("din functia json: ",steps_angles)
    # print(f"Body part: {body_part}, Angle: {angle}")
    # return ex.exercise(body_parts, steps_angles, permissive_error, count_max)

print(interpret_json(json_data))














#
# # Parse the JSON data
# data = json.loads(json_data_aux)
#
# # Extract the variables
# name = data["Name"]
# count_max = data["Count_max"]
# permissive_error = data["Permissive_error"]
#
# # Extract the arrays
# step_keys = list(data["Steps"].keys())  # ["step_0", "step_1"]
# step_values = list(data["Steps"].values())  # [{"RIGHT_ELBOW": 90, "LEFT_ELBOW": 90}, {"RIGHT_ELBOW": 180, "LEFT_ELBOW": 180}]
#
# # list
# body_parts = []
# # list of lists(steps)
# body_angles = []
#
# for step_dict in step_values:
#     current_step_body_angle = []
#     for body_part, corresponding_angle in step_dict.items():
#         if len(body_parts) == 0:
#             temp = var.find_variable_value(body_part)
#             if temp is None:
#                 print(f"No such Body Part -> {body_part}")
#                 break
#             body_parts.append(temp)
#             current_step_body_angle.append(int(corresponding_angle))
#         else:
#             current_step_body_angle.append(int(corresponding_angle))
#             body_angles.append(current_step_body_angle)
#
#
#
# # Print the variables and arrays
# print("Name:", name)
# print("Count_max:", count_max)
# print("Permissive_error:", permissive_error)
# print("Step keys:", step_keys)
# print("Step values:", step_values)
#
#
#
#










#
# def parse_json(data):
#     body_parts = []
#     steps_angles = []
#     if isinstance(data, dict):  # Check if the data is a dictionary
#         for key, value in data.items():
#             print(f"Key: {key}")
#
#             parse_json(value)  # Recursively parse nested values
#     elif isinstance(data, list):  # Check if the data is a list
#         for item in data:
#             parse_json(item)  # Recursively parse list items
#     else:
#         # print("hehe")
#         print(f"Value: {data}")
#
#
# # Parse the JSON data
# data = json.loads(json_data_aux)
#
# # Call the parse_json function
# parse_json(data)