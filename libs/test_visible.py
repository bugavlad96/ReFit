import cv2
import mediapipe as mp


mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose


# Define the point you want to check visibility for
point_id = 22  # Example: Right wrist (0-indexed)

# Initialize Mediapipe Pose
pose = mpPose.Pose()

# Open video capture
cap = cv2.VideoCapture(0)  # Use camera as the video source

while True:
    # Read frame from the video capture
    success, img = cap.read()

    # Convert the image to RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the image with Mediapipe Pose
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        # Draw the landmarks on the image
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        # Check if the desired point is visible
        if results.pose_landmarks.landmark[point_id].visibility > 0.5:
            cv2.circle(img, (int(results.pose_landmarks.landmark[point_id].x * img.shape[1]),
                            int(results.pose_landmarks.landmark[point_id].y * img.shape[0])),
                    10, (0, 255, 0), -1)
            print("yaaaaaaaaaaa")
            print(results.pose_landmarks.landmark[point_id].visibility)
        else:
            cv2.circle(img, (int(results.pose_landmarks.landmark[point_id].x * img.shape[1]),
                            int(results.pose_landmarks.landmark[point_id].y * img.shape[0])),
                    10, (0, 0, 255), -1)
            print("noooooooooo")
            print(results.pose_landmarks.landmark[point_id].visibility)
            

    # Display the image with landmarks
    cv2.imshow("Live Stream", img)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()



