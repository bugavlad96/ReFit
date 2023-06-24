import cv2
import libs.global_var as var
import mediapipe as mp

def prepare_stream(cap, pose):
    success, img = cap.read()
    img = cv2.resize(img, var.STREAM_RESIZE)

    # Create CUDA-based OpenCV matrix
    # d_img = cv2.cuda_GpuMat()
    # d_img.upload(img)
    #
    # # Convert CUDA-based GpuMat to CPU-based numpy array
    # img = d_img.download()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # results = pose.process(imgRGB)
    return img, pose.process(imgRGB)