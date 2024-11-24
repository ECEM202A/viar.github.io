import cv2
import mediapipe as mp
import numpy as np
import math

mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Initialize face mesh and pose models
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
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
    
    # Process face mesh and pose landmarks
    face_results = face_mesh.process(frame_rgb)
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

    face_coordination_in_real_world = np.array([
        [285, 528, 200],
        [285, 371, 152],
        [197, 574, 128],
        [173, 425, 108],
        [360, 574, 128],
        [391, 425, 108]
    ], dtype=np.float64)

    h, w, _ = frame.shape
    face_coordination_in_image = []

    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx in [1, 9, 57, 130, 287, 359]:
                    x, y = int(lm.x * w), int(lm.y * h)
                    face_coordination_in_image.append([x, y])

            face_coordination_in_image = np.array(face_coordination_in_image,
                                                  dtype=np.float64)

            # Use solvePnP function to get rotation vector
            success, rotation_vec, translation_vec = cv2.solvePnP(
                face_coordination_in_real_world, face_coordination_in_image,
                cam_matrix, dist_matrix)

            # Use Rodrigues function to convert rotation vector to matrix
            rotation_matrix, jacobian = cv2.Rodrigues(rotation_vec)

            result = rotation_matrix_to_angles(rotation_matrix)
            for i, info in enumerate(zip(('Pitch', 'Yaw', 'Roll'), result)):
                k, v = info
                text = f'{k}: {int(v)}'
                cv2.putText(frame, text, (20, i*30 + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Forward direction vector
            forward_vector = rotation_matrix @ np.array([0, 0, 1])

            nose_direction_point_3d = np.array([
                face_coordination_in_real_world[0][0] + forward_vector[0] * 1000,
                face_coordination_in_real_world[0][1] + forward_vector[1] * 1000,
                face_coordination_in_real_world[0][2] + forward_vector[2] * 1000
            ])

            print(f"Forward Vector: {forward_vector}")

            # Project the nose and direction point onto the 2D image plane
            nose_tip_2d, _ = cv2.projectPoints(
                np.array([face_coordination_in_real_world[0]]), rotation_vec, translation_vec, cam_matrix, dist_matrix
            )
            nose_direction_point_2d, _ = cv2.projectPoints(
                np.array([nose_direction_point_3d]), rotation_vec, translation_vec, cam_matrix, dist_matrix
            )

            # Draw the forward direction line starting at nose
            p1 = (int(nose_tip_2d[0][0][0]), int(nose_tip_2d[0][0][1]))
            p2 = (int(nose_direction_point_2d[0][0][0]), int(nose_direction_point_2d[0][0][1]))
            cv2.line(frame, p1, p2, (255, 0, 0), 2)


    # Draw pose landmarks for visualization
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow(" ", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
