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

The core of our system is the integration of the RealSense L515 depth camera, Apple Watch for haptic feedback, and auditory cues delivered through AirPods, all working cohesively to assist visually impaired individuals in object retrieval tasks. The RealSense L515 camera operates as a stationary depth-sensing device, providing real-time 3D mapping of the environment. This depth information is synchronized with RGB data to allow accurate object detection and spatial localization. Leveraging advanced computer vision techniques, such as YOLOv7 and MobileNetSSD models, the system identifies objects within the scene and deprojects their 2D positions into a 3D coordinate space using the camera's intrinsic parameters. This transformation is vital for determining the spatial relationships between the user and target objects.

To assist navigation, the system computes angles and vectors that represent the relative positions of the user’s head, hands, and the target object. Pose detection is achieved using the MediaPipe Pose Landmarker, which identifies key landmarks, including the user’s head and wrist positions. The head-object angle is computed using the following formula:

$$
\theta = \arccos \left( \frac{(x_2 - x_1)(x_3 - x_1) + (y_2 - y_1)(y_3 - y_1) + (z_2 - z_1)(z_3 - z_1)}{\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2} \cdot \sqrt{(x_3 - x_1)^2 + (y_3 - y_1)^2 + (z_3 - z_1)^2}} \right)
$$

Here, 
- \( (x_1, y_1, z_1) \) represents the coordinates of the user’s head,
- \( (x_2, y_2, z_2) \) represents the coordinates of the user’s current position,
- \( (x_3, y_3, z_3) \) represents the coordinates of the target object,
- and \( \theta \) is the computed angle.

The system applies this computation to generate directional commands, such as “move left” or “move forward,” which are refined using exponential moving averages to smooth out noisy data, ensuring reliable guidance in real time.

Haptic feedback delivered through the Apple Watch provides an intuitive method for users to locate objects. The system employs custom-designed haptic waveforms that vary in intensity based on the proximity of the user to the target object. Strong vibrations are triggered when the object is within 0.2 meters, medium vibrations at 1.0 meter, and weak vibrations at 1.5 meters. These patterns allow users to gauge their distance from the object without relying on visual cues. Commands are transmitted to the Apple Watch through an iPhone app using WCSession, which communicates with the laptop server via a UDP protocol. This seamless integration ensures low-latency feedback essential for real-time navigation.

Auditory feedback complements the haptic signals by guiding macro-level movements toward the target object. Using speech-to-text functionality, users can issue commands such as “find my keys,” which the system processes to initiate object detection and spatial analysis. Directional audio cues, synchronized with haptic feedback, are delivered through AirPods, providing users with clear and actionable instructions. This dual-modal feedback system significantly enhances the user experience by addressing both macro and micro navigation challenges.

The system’s hand tracking capability is another critical component, enabling precise object retrieval. By deprojecting wrist landmarks into 3D space, the system calculates the Euclidean distance between the user’s hand and the target object. This information guides fine motor movements required for grasping objects. Noise and inaccuracies in the depth data are mitigated using filtering techniques and majority-voting mechanisms, which improve the overall reliability of the system.

The modular design of the system allows each component—the depth camera, laptop server, mobile application, and wearable devices—to operate independently while maintaining seamless communication. This modularity not only simplifies debugging and updates but also ensures the system's scalability and adaptability to various use cases. The RealSense camera streams spatial data to a laptop server, which processes the information and transmits commands to the iPhone app. The app, in turn, relays these commands to the Apple Watch and AirPods, creating a cohesive and efficient navigation framework for visually impaired individuals.

---

# 4. Evaluation and Results

The evaluation of the system focused on its ability to accurately compute head, object, and hand positioning and provide effective real-time guidance through multi-modal feedback. The RealSense L515 depth camera demonstrated high precision in spatial mapping, enabling the system to generate reliable directional commands. By combining angle and vector computations, the system provided users with accurate instructions for both macro navigation and micro adjustments required for object retrieval. During controlled trials, auditory feedback proved effective in guiding users toward target objects, while haptic signals played a crucial role in confirming object proximity.

Haptic feedback performance was assessed through 20 trials, where users were tasked with locating objects within a 1-meter radius. The system achieved a success rate of 70%, demonstrating its capability to provide meaningful guidance. Feedback intensity scaling was validated at three distance thresholds: strong feedback at 0.2 meters, medium feedback at 1.0 meter, and weak feedback at 1.5 meters. Although effective, further refinement in haptic feedback patterns is necessary to enhance guidance for wrist-level micro-movements. The integration of filtering mechanisms and majority-voting systems significantly improved the reliability of the feedback loop by reducing noise and ensuring consistent performance across various scenarios.

Latency analysis revealed an average UDP round-trip time of 8.0 milliseconds, with a range of 6.8 to 9.2 milliseconds across all trials. This low latency underscores the system’s capability to deliver real-time responses essential for navigation. The total delay from auditory command initiation to haptic feedback delivery, encompassing all computational and communication processes, was measured at 3.53 seconds. This result highlights the system’s responsiveness and its potential for real-world applications.

Distance feedback calibration further validated the system's ability to provide precise proximity-based guidance. Strong vibrations at 0.2 meters effectively signaled the user’s arrival at the target, while medium and weak vibrations at greater distances provided gradual directional cues. These calibrated responses ensured that users could confidently approach and retrieve objects without relying on visual input. Additionally, the combination of haptic and auditory feedback proved instrumental in facilitating seamless navigation and object localization.

Overall, the system demonstrated robust performance in assisting visually impaired individuals with object retrieval tasks. Its high accuracy, low latency, and effective multi-modal feedback make it a promising solution for enhancing independence and mobility. However, ongoing improvements in haptic feedback design and adaptive algorithms will further optimize the system’s usability and effectiveness in diverse environments.

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

6. Live Speech-to-text Apple Framework: https://developer.apple.com/documentation/speech/
