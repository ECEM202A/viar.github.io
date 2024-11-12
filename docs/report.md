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

### Challenges
Key challenges include ensuring the accuracy and responsiveness of object detection, developing intuitive haptic feedback patterns, and adapting the system for various indoor environments with different lighting and layouts.

### Requirements for Success
The project requires expertise in computer vision, real-time data processing, haptic feedback design, and software integration. Hardware components include the RealSense L515, Apple Watch, and audio devices like AirPods. 

### Metrics of Success
- **Accuracy**: Correctly identified and localized objects.
- **Response Time**: Speed from user request to successful object retrieval.
- **User Satisfaction**: Feedback from user testing.
- **Reliability**: System performance in different environments.
- **Ease of Use**: User adaptability to the system.

---

# 2. Related Work

- *Using Depth Cameras for Object Detection and Navigation Assistance for the Visually Impaired*: Discusses mapping environments using depth cameras to support navigation and object detection.
- *Haptic Feedback for Object Localization and Grasping in Assistive Technologies*: Explores haptic feedback for guiding users in object retrieval, which is essential in our approach with the Apple Watch.
- *Speech Recognition Systems in Assistive Technologies*: Reviews voice-controlled systems for visually impaired users, which inspired our hands-free control through voice commands.
- *Moving Object Detection in RGBD Data*: Highlights techniques like background subtraction and motion detection, relevant to our use of RGB-D data for spatial guidance.
- *Holistic Scene Understanding for 3D Object Detection with RGBD Cameras*: Discusses integration of RGB and depth data for more comprehensive scene understanding.

---

# 3. Technical Approach

(Include a brief description of your current setup, with the RealSense L515 camera, Apple Watch haptic feedback, and ongoing development of hand tracking and object detection.)

---

# 4. Evaluation and Results

(Add details on your evaluation metrics and any initial results here.)

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
