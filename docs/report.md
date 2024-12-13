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

<p align="center">
  <img src="https://github.com/user-attachments/assets/ba2591b9-508e-42e5-b2a8-3da9dc7d8f6b" width="75%" />
</p>

*Figure 1: Overview of the app structure, showcasing the components and interactions between hardware and software modules.*

### Novelty & Rationale
Our approach utilizes a stationary RealSense L515 depth camera combined with haptic feedback from an Apple Watch and auditory cues. This setup provides a hands-free experience, avoiding the discomfort of head-mounted devices. The integration of depth sensing, haptic, and auditory feedback ensures accurate object retrieval and intuitive navigation, making the system practical for everyday use.

---

# 2. Related Work

<p align="center">
  <img src="https://github.com/user-attachments/assets/93daf982-5c00-4463-8f38-257b3708db80" width="30%" />
</p>

*Figure 2: An example of the phone app interface designed to integrate with the RealSense system and provide seamless interaction.*

- *Using Depth Cameras for Object Detection and Navigation Assistance for the Visually Impaired*: Discusses mapping environments using depth cameras to support navigation and object detection.
- *Haptic Feedback for Object Localization and Grasping in Assistive Technologies*: Explores haptic feedback for guiding users in object retrieval, which is essential in our approach with the Apple Watch.
- *Speech Recognition Systems in Assistive Technologies*: Reviews voice-controlled systems for visually impaired users, which inspired our hands-free control through voice commands.
- *Moving Object Detection in RGBD Data*: Highlights techniques like background subtraction and motion detection, relevant to our use of RGB-D data for spatial guidance.
- *Holistic Scene Understanding for 3D Object Detection with RGBD Cameras*: Discusses integration of RGB and depth data for more comprehensive scene understanding.

---

# 3. Technical Approach

The core of our system is the integration of the RealSense L515 depth camera, Apple Watch for haptic feedback, and auditory cues delivered through AirPods, all working cohesively to assist visually impaired individuals in object retrieval tasks. The RealSense L515 camera operates as a stationary depth-sensing device, providing real-time 3D mapping of the environment. This depth information is synchronized with RGB data to allow accurate object detection and spatial localization. Leveraging advanced computer vision techniques, such as YOLOv7 and MobileNetSSD models, the system identifies objects within the scene and deprojects their 2D positions into a 3D coordinate space using the camera's intrinsic parameters. This transformation is vital for determining the spatial relationships between the user and target objects.

<p align="center">
  <img src="https://github.com/user-attachments/assets/483e058e-e768-4a13-9437-8d24ff0012e4" width="75%" />
</p>

*Figure 3: RealSense L515 setup illustrating its position for optimal depth sensing.*

To assist navigation, the system computes angles and vectors that represent the relative positions of the user’s head, hands, and the target object. Pose detection is achieved using the MediaPipe Pose Landmarker, which identifies key landmarks, including the user’s head and wrist positions. The spatial angle is computed using the following formula:

$$
\text{Head}_{\text{angle}} = 180 + \arctan\left(\frac{x_{\text{head vector}}}{z_{\text{head vector}}}\right)
$$


This formula determines the precise direction of the user’s head relative to the target object by using the components of the head vector in 3D space. Together, these calculations generate directional commands, such as "move left" or "move forward," which are refined using exponential moving averages to smooth out noisy data, ensuring reliable guidance in real time.

<p align="center">
  <img src="https://github.com/user-attachments/assets/c6633245-69ba-4903-9221-c448b05ba963" width="75%" />
</p>

*Figure 4: Visualization of head-object angle computation for navigation guidance.*

Haptic feedback delivered through the Apple Watch provides an intuitive method for users to locate objects. The system employs custom-designed haptic waveforms that vary in intensity based on the proximity of the user to the target object. Strong vibrations are triggered when the object is within 0.2 meters, medium vibrations at 1.0 meter, and weak vibrations at 1.5 meters. These patterns allow users to gauge their distance from the object without relying on visual cues. Commands are transmitted to the Apple Watch through an iPhone app using WCSession, which communicates with the laptop server via a UDP protocol.

<p align="center">
  <img src="https://github.com/user-attachments/assets/9d4a343c-f6f7-4003-a618-371a2e038229" width="30%" />
</p>

*Figure 5: Haptic feedback patterns displayed on the Apple Watch UI.*

---

# 4. Evaluation and Results

The evaluation of the system focused on its ability to accurately compute head, object, and hand positioning and provide effective real-time guidance through multi-modal feedback. The RealSense L515 depth camera demonstrated high precision in spatial mapping, enabling the system to generate reliable directional commands. By combining angle and vector computations, the system provided users with accurate instructions for both macro navigation and micro adjustments required for object retrieval. During controlled trials, auditory feedback proved effective in guiding users toward target objects, while haptic signals played a crucial role in confirming object proximity.

<p align="center">
  <img src="https://github.com/user-attachments/assets/f4f0fde8-e58a-4d36-b286-88b3eac58faa" width="75%" />
</p>

*Figure 6: Depth distancing test showing the system's ability to calculate object distances with high precision.*

The results demonstrated that the integration of filtering mechanisms significantly improved the reliability of the feedback loop by reducing noise and ensuring consistent performance across various scenarios. Additionally, the low latency of 8 milliseconds for UDP round-trip responses underscores the system’s potential for real-time applications. User feedback highlighted the accuracy of auditory cues for macro navigation and the effectiveness of haptic feedback in indicating proximity to target objects.

---

# 5. Discussion and Conclusions

The system successfully integrates object keyword recognition and YOLO-based object detection, enabling seamless identification of target objects alongside accurate computation of head, object, and hand positioning. Precise angle and vector calculations generate reliable directional audio feedback, which effectively guides users toward objects during macro movements and helps them navigate their environment. Haptic feedback indicates proximity but could benefit from greater nuance to guide micro-movements, such as aligning the wrist with the object. Additionally, filtering mechanisms and majority-voting systems improve the reliability of real-time feedback by reducing noise, ensuring consistent and accurate guidance, and making the system a promising assistive tool for visually impaired individuals.

Future directions involve improving the granularity of haptic feedback patterns to better support wrist-level movements and optimizing speech recognition algorithms for faster response times. Integration with additional wearable devices could further enhance the system’s usability and adaptability.

---

# 6. References

1. *Using Depth Cameras for Object Detection and Navigation Assistance for the Visually Impaired*  
   URL: https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9795125

2. *Haptic Feedback for Object Localization and Grasping in Assistive Technologies*  
   URL: https://dl.acm.org/doi/abs/10.1145/2982142.2982160

3. *Moving Object Detection in RGBD Data*  
   URL: https://www.mdpi.com/2313-433X/4/5/71

4. *Holistic Scene Understanding for 3D Object Detection with RGBD Cameras*  
   URL: https://openaccess.thecvf.com/content_iccv_2013/papers/Lin_Holistic_Scene_Understanding_2013_ICCV_paper.pdf

5. *FusionVision: 3D Object Reconstruction with RGB-D Cameras*  
   URL: https://www.mdpi.com/1424-8220/24/9/2889

6. *Live Speech-to-text Apple Framework*  
   URL: https://developer.apple.com/documentation/speech/