import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Path to pose model
MODEL_PATH = os.path.expanduser('~/OneDrive/Desktop/UCLA Q1/ECE M202A/Project/pose_landmarker.task')

def initialize_pose_landmarker():
    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=True
    )
    return vision.PoseLandmarker.create_from_options(options)

def detect_pose_landmarks(image_path, detector):
    image = mp.Image.create_from_file(image_path)
    return detector.detect(image), image

# RGB image array
def detect_pose_landmarks_from_array(rgb_image, detector):
    # Convert RGB image array to MediaPipe Image format
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
    return detector.detect(mp_image)

def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    for idx, pose_landmarks in enumerate(pose_landmarks_list):
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
            for landmark in pose_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style()
        )

        # Add landmark indices as numbers
        for i, landmark in enumerate(pose_landmarks):
            x = int(landmark.x * rgb_image.shape[1])
            y = int(landmark.y * rgb_image.shape[0])
            cv2.putText(
                annotated_image, str(i), (x, y), 
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=0.4, 
                color=(255, 0, 0), 
                thickness=1, 
                lineType=cv2.LINE_AA
            )
            
    return annotated_image

if __name__ == "__main__":

    # Init PoseLandmarker
    detector = initialize_pose_landmarker()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
    else:
        while cv2.waitKey(1) != ord('q'):
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not capture frame.")
                break

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect and draw landmarks from the frame
            detection_result = detect_pose_landmarks_from_array(img_rgb, detector)
            annotated_image = draw_landmarks_on_image(img_rgb, detection_result)

            # Check if landmarks are detected
            if detection_result.pose_landmarks:
                # Get index value for the nose
                nose_index = mp.solutions.pose.PoseLandmark.NOSE.value

                # Access the nose landmark
                nose = detection_result.pose_landmarks[0][nose_index]

                # Print the z-value for the nose
                print(f"Nose Z: {nose.z:.2f}")
            else:
                print("Nose landmark not detected.")

            annotated_image_bgr = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)

            cv2.imshow("Pose Detection", annotated_image_bgr)

        cap.release()
        cv2.destroyAllWindows()