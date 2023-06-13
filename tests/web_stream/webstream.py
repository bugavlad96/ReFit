import cv2
from flask import Flask, Response, render_template



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

app = Flask(__name__)

# def exercise(body_parts, steps_angles, permissive_error, count_max):
#     # TREBUIE DE BAGAT TOT WHILE TRUE-ul pentru ca sa se execute aici!!!!!!!!!!!!!!!!!!
#
#     # --------------------------------------------------------------------------------------------------
#     # --------------------------------------------------------------------------------------------------
#
#     # initialize some vars
#     up = False
#
#     counter = 0
#     are_steps_completed = []
#     actual_values = []
#
#     first_half_exercise = False
#     second_half_exercise = False
#
#     # for idx in range(len(body_parts)):
#     #     are_steps_completed[idx] = var.STEP_NOT_COMPLETED
#     are_steps_completed = [False for _ in range(len(steps_angles))]
#     actual_values = [-1 for _ in range(len(steps_angles))]
#
#     cv2.setUseOptimized(True)
#     cv2.cuda.setDevice(0)
#
#     # Create MediaPipe objects
#     mpDraw = mp.solutions.drawing_utils
#     mpPose = mp.solutions.pose
#     pose = mpPose.Pose()
#
#     cap = cv2.VideoCapture(0)  # Use camera as the video source
#
#     while True:
#
#         success, img = cap.read()
#         img = cv2.resize(img, var.STREAM_RESIZE)
#
#         # Create CUDA-based OpenCV matrix
#         d_img = cv2.cuda_GpuMat()
#         d_img.upload(img)
#
#         # Convert CUDA-based GpuMat to CPU-based numpy array
#         img = d_img.download()
#
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         results = pose.process(imgRGB)
#
#         # the condition will be True if at least one pose landmark is detected.
#         # aici poti verifica daca faci displaty doar la landmark-urile relevante sau le lasi pe toate
#         if results.pose_landmarks:
#             # printeaza punctele si conexiunile. Oferit de mdedia pipe
#             mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
#             points = utils.collect_points(img, results)
#
#             if not first_half_exercise:
#                 print("am intrat")
#                 for idx, is_step_completed in enumerate(are_steps_completed):
#
#                     if (not is_step_completed):
#                         # print(idx, is_step_completed)
#                         print(f"index {idx}")
#                         are_steps_completed[idx], actual_values[idx] = step.step(results, img, body_parts,
#                                                                                  steps_angles[idx], permissive_error)
#                         if not are_steps_completed[idx]:
#                             print(f"{idx} NOT completed")
#                             break
#                         else:
#                             print(f"{idx}  SUCCESS")
#                             if idx == len(are_steps_completed) - 1:
#                                 print("the last step up")
#                                 first_half_exercise = True
#
#                                 print(counter)
#                                 are_steps_completed = [False for _ in range(len(steps_angles))]
#
#             if first_half_exercise:
#                 print("in intrat in sens invers")
#
#                 for idx, is_step_completed in reversed(list(enumerate(are_steps_completed))):
#                     if (not is_step_completed):
#                         are_steps_completed[idx], actual_values[idx] = step.step(results, img, body_parts,
#                                                                                  steps_angles[idx], permissive_error)
#                         if not are_steps_completed[idx]:
#                             print(f"{idx} NOT completed")
#                             break
#                         else:
#                             print(f"{idx}  SUCCESS")
#                             if idx == 0:
#                                 print("the last step dowm")
#                                 counter += 1
#                                 first_half_exercise = False
#                                 # second_half_exercise = True
#                                 are_steps_completed = [False for _ in range(len(steps_angles))]
#
#             if counter == count_max:
#                 break
#
#             print("--------------")
#
#         ot.output_text(img, str(counter), var.FISRT_LANE, var.RED, var.SIZE_TXT_HINTS)
#         # cv2.putText(img, str(counter), (100, 150), cv2.FONT_HERSHEY_PLAIN, 12, (255, 0, 0), 12)
#         _, encoded_frame = cv2.imencode('.jpg', img)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_frame) + b'\r\n')
#     #     cv2.imshow("img", img)
#     #     if cv2.waitKey(1) & 0xFF == ord('q'):
#     #         break
#     #
#     # cap.release()
#     # cv2.destroyAllWindows()
#
#     # return counter


# def generate_frames():
#
#
#
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#
#
#         _, encoded_frame = cv2.imencode('.jpg', frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_frame) + b'\r\n')
import core.exercise as ex
body_parts = [var.LEFT_ELBOW, var.RIGHT_ELBOW, var.LEFT_SHOULDER, var.RIGHT_SHOULDER]
steps = [[var.ANGLE_170, var.ANGLE_170, var.ANGLE_110, var.ANGLE_110],
         [var.ANGLE_170, var.ANGLE_170, var.ANGLE_140, var.ANGLE_140],
         [var.ANGLE_170, var.ANGLE_170, var.ANGLE_160, var.ANGLE_160],
         [var.ANGLE_170, var.ANGLE_170, var.ANGLE_180, var.ANGLE_180]]
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(ex.exercise(body_parts, steps, var.ERROR_10, 4), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
