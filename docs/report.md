# Table of Contents
* Abstract
* [Introduction](#1-introduction)
* [Related Work](#2-related-work)
* [Technical Approach](#3-technical-approach)
* [Evaluation and Results](#4-evaluation-and-results)
* [Discussion and Conclusions](#5-discussion-and-conclusions)
* [References](#6-references)

---

# Abstract

This project aims to create an object retrieval system for visually impaired individuals using a depth camera (RealSense L515), Apple Watch for haptic feedback, and auditory cues. The system provides spatial awareness and real-time navigational guidance, allowing users to locate and retrieve objects with precision. Our approach integrates stationary depth sensing with multi-modal feedback, offering a hands-free, comfortable solution. Initial results show that haptic feedback is functional, and object detection and hand tracking capabilities are under development.

---

# 1. Introduction

### Motivation & Objective
Our project seeks to enhance independence for visually impaired individuals by providing a system that offers precise spatial guidance for locating objects in a room. This system uses haptic and auditory feedback to guide users, helping them retrieve objects like keys or a phone without assistance.

### State of the Art & Its Limitations
Currently, assistive technologies like Seeing AI and BlindSquare use computer vision and audio cues for basic navigation and object identification. Head-mounted devices and wearable cameras have been explored but can be uncomfortable for prolonged use. Existing systems often lack multi-modal feedback, making spatial navigation less intuitive for users.

### Novelty & Rationale
Our approach utilizes a stationary RealSense L515 depth camera combined with haptic feedback from an Apple Watch and auditory cues. This setup provides a hands-free experience, avoiding the discomfort of head-mounted devices. The integration of depth sensing, haptic, and auditory feedback ensures accurate object retrieval and intuitive navigation, making the system practical for everyday use.

### Potential Impact
If successful, this system will significantly improve the autonomy of visually impaired individuals by enabling them to navigate indoor spaces and retrieve objects independently. Technologically, it demonstrates an innovative integration of depth sensing with multi-modal feedback in assistive applications.

---

# 2. Related Work

- *Using Depth Cameras for Object Detection and Navigation Assistance for the Visually Impaired*: Discusses mapping environments using depth cameras to support navigation and object detection.
- *Haptic Feedback for Object Localization and Grasping in Assistive Technologies*: Explores haptic feedback for guiding users in object retrieval, which is essential in our approach with the Apple Watch.
- *Speech Recognition Systems in Assistive Technologies*: Reviews voice-controlled systems for visually impaired users, which inspired our hands-free control through voice commands.
- *Moving Object Detection in RGBD Data*: Highlights techniques like background subtraction and motion detection, relevant to our use of RGB-D data for spatial guidance.
- *Holistic Scene Understanding for 3D Object Detection with RGBD Cameras*: Discusses integration of RGB and depth data for more comprehensive scene understanding.

---

# 3. Technical Approach

### Depth Camera Integration (RealSense L515)
The stationary RealSense L515 depth camera is the core of our system, enabling real-time 3D mapping of the environment. It captures synchronized RGB and depth data to localize objects in the room. 
- **Object Detection**: Implemented using YOLOv7 and MobileNetSSD models. Detected 2D object coordinates are deprojected into 3D points using camera intrinsics and depth data.
- **Pose Detection**: MediaPipe Pose Landmarker identifies user pose landmarks, such as eyes, nose, hands, and wrists, for navigation and retrieval tasks.
- **Data Processing**: The camera streams data to a laptop server, which processes it for spatial calculations and guidance instructions.

### Spatial Angle and Vector Calculations
- **Head-Object Angle**: The 3D position of the head (derived from MediaPipe landmarks) is compared with the object’s 3D position. Angles are computed using vector mathematics to determine the user’s relative orientation.
- **Directional Commands**: By comparing the head-object angle and the forward head angle, the system generates directional instructions such as “left,” “right,” or “forward.” Exponential moving averages smooth noisy data to improve reliability.

### Haptic Feedback via Apple Watch
- **Implementation**: Custom haptic waveforms are created using the Taptic Engine to deliver feedback based on proximity to the object.
  - Strong vibration: Within 0.2 meters.
  - Medium vibration: Within 1.0 meter.
  - Weak vibration: Within 1.5 meters.
- **Communication**: Commands are sent to the Apple Watch via WCSession from an iPhone app, which communicates with the laptop server using UDP.

### Auditory Feedback via AirPods
- **Speech Recognition**: Users issue commands like “find my keys” via speech-to-text. Recognized commands trigger scene analysis by the server.
- **Directional Audio**: Spatial audio cues guide users to objects. Commands such as “left,” “right,” or “forward” are played dynamically based on real-time positional data.
- **Integration**: Audio instructions are synchronized with haptic feedback for seamless navigation.

### Object and Hand Tracking
- **Hand-Object Vector**: Wrist positions are tracked using MediaPipe and deprojected into 3D space. The system computes the Euclidean distance between the hand and the object to guide precise retrieval movements.
- **Enhancements**: Filtering techniques and majority-voting mechanisms are used to reduce noise and improve accuracy in hand tracking.

### System Integration
Our system integrates multiple components to provide a cohesive user experience:
- **Depth Camera and Server**: The RealSense camera sends spatial data to a laptop, which processes object localization, head angles, and directional commands.
- **Mobile and Wearable Devices**: The iPhone app acts as an intermediary, relaying commands to the Apple Watch for haptic feedback and AirPods for audio guidance.
- **Modularity**: Each component (camera, server, phone, watch) operates independently but communicates seamlessly for scalability and flexibility.

---

# 4. Evaluation and Results
The system demonstrates effective computation of head, object, and hand positioning and orientation, providing accurate directional guidance for users. Angle and vector computations generate reliable directional commands, while audio feedback effectively guides macro movements toward the target object. Haptic feedback is useful for object localization, achieving 70% success in guiding users to locate objects within a 1-meter radius across 20 trials. However, the haptic feedback could be further refined to provide more nuanced guidance for wrist-level micro-movements. Filtering and majority voting systems improve the reliability of directional commands by reducing noise in the real-time feedback control loop.

Performance metrics indicate an average UDP round-trip latency of 8.0 milliseconds, with a range of 6.8 to 9.2 milliseconds across 20 trials. Distance feedback calibration was validated, showing appropriate vibration intensity scaling at 0.2m (strong feedback), 1.0m (medium feedback), and 1.5m (weak feedback). The total delay from auditory command to wrist feedback, encompassing multiple devices and computations, was measured at 3.53 seconds. These results highlight the system’s responsiveness and effectiveness at assisting in object retrieval and real-time guidance.

---

# 5. Discussion and Conclusions
(Summarize findings and potential future directions.)

---

# 6. References

1. *Using Depth Cameras for Object Detection and Navigation Assistance for the Visually Impaired*
   - URL: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9795125

2. *Haptic Feedback for Object Localization and Grasping in Assistive Technologies*
   - URL: https://dl.acm.org/doi/abs/10.1145/2982142.2982160

3. *Moving Object Detection in RGBD Data*
   - URL: https://www.mdpi.com/2313-433X/4/5/71

4. *Holistic Scene Understanding for 3D Object Detection with RGBD Cameras*
   - URL: https://openaccess.thecvf.com/content_iccv_2013/papers/Lin_Holistic_Scene_Understanding_2013_ICCV_paper.pdf

5. *FusionVision: 3D Object Reconstruction with RGB-D Cameras*
   - URL: https://www.mdpi.com/1424-8220/24/9/2889