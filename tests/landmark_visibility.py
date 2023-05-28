import cv2
import mediapipe as mp

# Initialize Mediapipe Pose
mpPose = mp.solutions.pose
pose = mpPose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize OpenCV VideoCapture
cap = cv2.VideoCapture(0)

# Get the number of landmarks
num_landmarks = len(mpPose.POSE_CONNECTIONS)

# Flag to track if indices are printed
indices_printed = False

while True:
    success, img = cap.read()

    # Convert the image to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the image with Mediapipe Pose
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            if id < num_landmarks:
                # Print the landmark object for inspection
                print("Landmark {}: {}".format(id, lm))

    # Print the index of landmarks once
    if not indices_printed:
        for id in range(num_landmarks):
            print("Landmark {}: {}".format(id, id))  # Corrected the print statement
        indices_printed = True

    cv2.imshow("Live Stream", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
