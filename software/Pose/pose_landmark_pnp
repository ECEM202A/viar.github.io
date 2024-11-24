import cv2
import mediapipe as mp
import numpy as np
import math

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Initialize pose model
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Camera parameters
focal_length = 1.0 * cap.get(3)  # width of the frame
camera_matrix = np.array([
    [focal_length, 0, cap.get(3) / 2],
    [0, focal_length, cap.get(4) / 2],
    [0, 0, 1]
], dtype="double")
dist_coeffs = np.zeros((4, 1), dtype=np.float64)

# Function to convert rotation matrix to Euler angles
def rotation_matrix_to_angles(rotation_matrix):
    x = math.atan2(rotation_matrix[2, 1], rotation_matrix[2, 2])
    y = math.atan2(-rotation_matrix[2, 0], math.sqrt(rotation_matrix[0, 0] ** 2 + rotation_matrix[1, 0] ** 2))
    z = math.atan2(rotation_matrix[1, 0], rotation_matrix[0, 0])
    return np.array([x, y, z]) * 180. / math.pi

while True:
    success, frame = cap.read()
    if not success:
        continue

    # RGB for MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process pose landmarks
    pose_results = pose.process(frame_rgb)

    # BGR for OpenCV
    frame_rgb = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    # Camera matrix
    focal_length = 1 * cap.get(3)
    cam_matrix = np.array([[focal_length, 0, cap.get(3) / 2],
                            [0, focal_length, cap.get(4) / 2],
                            [0, 0, 1]])

    # Distortion matrix
    dist_matrix = np.zeros((4, 1), dtype=np.float64)

    # Define real-world coordinates for pose landmarks
    # Coordinates are in meters and approximate human proportions
    pose_coordination_in_real_world = np.array([
        [0, 0, 0],        # Nose
        [-0.1, 0.2, 0],   # Left eye
        [0.1, 0.2, 0],    # Right eye
        [-0.3, 0.4, 0],   # Left shoulder
        [0.3, 0.4, 0],    # Right shoulder
        [-0.2, 0.8, 0],   # Left hip
        [0.2, 0.8, 0]     # Right hip
    ], dtype=np.float64)

    h, w, _ = frame.shape
    pose_coordination_in_image = []

    if pose_results.pose_landmarks:
        
        

        landmarks = pose_results.pose_landmarks.landmark
        indices = [
            mp_pose.PoseLandmark.NOSE,
            mp_pose.PoseLandmark.LEFT_EYE,
            mp_pose.PoseLandmark.RIGHT_EYE,
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.RIGHT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.RIGHT_HIP
        ]

                # Get key points
        nose = np.array([landmarks[mp_pose.PoseLandmark.NOSE].x * w,
                         landmarks[mp_pose.PoseLandmark.NOSE].y * h,
                         landmarks[mp_pose.PoseLandmark.NOSE].z])

        left_eye = np.array([landmarks[mp_pose.PoseLandmark.LEFT_EYE].x * w,
                             landmarks[mp_pose.PoseLandmark.LEFT_EYE].y * h,
                             landmarks[mp_pose.PoseLandmark.LEFT_EYE].z])

        right_eye = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_EYE].x * w,
                              landmarks[mp_pose.PoseLandmark.RIGHT_EYE].y * h,
                              landmarks[mp_pose.PoseLandmark.RIGHT_EYE].z])

        # Compute eye center
        eye_center = (left_eye + right_eye) / 2

        # Compute manual forward vector (nose to eye center)
        manual_forward_vector = eye_center - nose
        # Remove the vertical (Y-axis) component
        manual_forward_vector[1] = 0  # Set Y-component to 0

        # Normalize the horizontal vector
        horizontal_vector = manual_forward_vector / np.linalg.norm(manual_forward_vector)

        horizontal_vector = -horizontal_vector

        # Project the manual forward vector
        manual_forward_point = np.array([
            nose[0] - manual_forward_vector[0] * 10,  # Extend for visualization
            nose[1],# + manual_forward_vector[1] * 100,
            nose[2] + manual_forward_vector[2] * 10
        ])

        print(f"Forward Vector: {manual_forward_vector}")

        # Draw the manual forward vector
        p1_manual = (int(nose[0]), int(nose[1]))
        p2_manual = (int(manual_forward_point[0]), int(manual_forward_point[1]))
        cv2.line(frame, p1_manual, p2_manual, (0, 255, 0), 2)  # Green line for manual vector
    

    # Draw pose landmarks for visualization
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Pose Estimation with solvePnP", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
