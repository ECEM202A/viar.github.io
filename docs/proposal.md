# Project Proposal

## 1. Motivation & Objective

This project aims to assist visually impaired individuals in achieving spatial awareness and navigational guidance. By combining a depth camera, Apple Watch, and auditory feedback, the system provides precise object retrieval instructions. The Apple Watch delivers haptic feedback, while auditory cues offer real-time navigation and guidance, enhancing independence in locating and grasping objects.

## 2. State of the Art & Its Limitations

Currently, assistive technologies like Seeing AI, Autour, and BlindSquare provide limited navigational or object detection assistance using either vision or audio alone. Head-mounted depth cameras have been explored but can be cumbersome, and current systems often lack intuitive, multi-modal feedback for accurate object retrieval.

## 3. Novelty & Rationale

Our approach integrates a stationary depth camera (RealSense L515), Apple Watch haptic feedback, and auditory cues to provide a more intuitive and comfortable solution. By leveraging stationary depth sensing and hands-free, multi-modal feedback, this system promises higher accuracy in navigation and object retrieval, without the discomfort of wearable headgear. We believe this comprehensive setup will significantly improve user experience and reliability.

## 4. Potential Impact

If successful, this system will provide a major improvement in spatial awareness and object retrieval for visually impaired individuals. Technically, it will demonstrate the integration of depth sensing, haptic feedback, and auditory guidance. Broadly, it has the potential to enhance accessibility tools, offering users greater autonomy and confidence in navigating their environments.

## 5. Challenges

Key challenges include:
- Ensuring real-time, accurate object detection and localization.
- Developing intuitive haptic and auditory feedback that is easy for users to interpret.
- Overcoming limitations in depth camera performance under varying lighting and room layouts.

## 6. Requirements for Success

Necessary skills and resources:
- **Technical Skills**: Proficiency in computer vision, haptic feedback design, and real-time processing.
- **Hardware**: RealSense L515 depth camera, Apple Watch, and audio feedback devices (e.g., AirPods).
- **Software**: Object recognition, path planning, and natural language processing algorithms.
  
## 7. Metrics of Success

Metrics for success include:
- **Accuracy**: Correctly identified and localized objects.
- **Response Time**: Speed from user request to successful object retrieval.
- **User Satisfaction**: Feedback from visually impaired users testing the prototype.
- **Reliability**: Consistency across different environments and conditions.
- **Ease of Use**: Time taken by users to learn and effectively use the system.

## 8. Execution Plan

### Key Tasks
1. Set up depth camera and Apple Watch integration.
2. Develop object/orientation detection and tracking algorithms.
3. Implement haptic and auditory feedback systems.
4. Conduct user testing and iterate on feedback.

### Team Task Partitioning
- **Arshia Dabiran**: Depth Camera Setup/Laptop-iOS interface
- **Alex Haafemeister**: Object/Orientation detection and tracking algorithms.
- **Dhruv Sirohi**: Speech recognition system,keyword detection, integration with the navigation pipeline
- **Yiteng Jiang**: Developed the watch and phone apps, integrating UDP communication and audio/haptic feedback for navigation.



## 9. Related Work

### 9.a. Papers
1. *Using Depth Cameras for Object Detection and Navigation Assistance for the Visually Impaired*  
   Discusses mapping environments and aiding in object detection using depth cameras.

2. *Haptic Feedback for Object Localization and Grasping in Assistive Technologies*  
   Explores the role of haptic feedback in guiding users toward objects accurately.

3. *Speech Recognition Systems in Assistive Technologies: Navigating and Retrieving Objects*  
   Reviews voice-controlled systems for navigation and object interaction.  
   [Link](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9795125)  
   [Link](https://dl.acm.org/doi/abs/10.1145/2982142.2982160)

4. *Moving Object Detection in RGBD Data*  
   Highlights techniques for background subtraction and motion detection using RGB-D cameras.  
   [Link](https://www.mdpi.com/2313-433X/4/5/71)

5. *Holistic Scene Understanding for 3D Object Detection with RGBD Cameras*  
   Discusses methods for integrating RGB and depth data for indoor environments.  
   [Link](https://openaccess.thecvf.com/content_iccv_2013/papers/Lin_Holistic_Scene_Understanding_2013_ICCV_paper.pdf)

### 9.b. Datasets
1. **Intel RealSense Path Planning Dataset**  
   [Link](https://github.com/pancx/pathplanning)

2. **Object Detection and Navigation Dataset**  
   Custom dataset based on user testing and room mapping data.

### 9.c. Software
1. **Intel RealSense SLAM Library**: For real-time object localization.  
   [Link](https://www.jstage.jst.go.jp/article/jsp/23/4/23_201/_pdf/-char/en)

2. **Whisper OpenAI**: For speech recognition and natural language processing.  
   [Link](https://developer.apple.com/tutorials/app-dev-training/transcribing-speech-to-text)

## 10. References
1. Depth Cameras in Assistive Tech: Paper: "Using Depth Cameras for Object Detection and Navigation Assistance for the Visually Impaired" Discusses how depth cameras can map environments and aid in object detection and navigation.

2. Haptic Feedback in Object Retrieval: Paper: "Haptic Feedback for Object Localization and Grasping in Assistive Technologies" Explores how haptic feedback can be used to guide users towards precise movements for object retrieval.

3. Speech Recognition in Assistive Devices: Paper: "Speech Recognition Systems in Assistive Technologies: Navigating and Retrieving Objects" Reviews the use of voice-controlled systems for visually impaired navigation and object interaction. https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9795125 https://dl.acm.org/doi/abs/10.1145/2982142.2982160

4. Moving Object Detection: www.mdpi.com/2313-433X/4/5/71: Paper: Moving Object Detection in RGBD Data Summary: Surveys background subtraction techniques for detecting moving objects using RGB-D cameras, highlighting the role of depth data in improving object detection accuracy.

5. Room Scanning Paper: Holistic Scene Understanding for 3D Object Detection with RGBD Cameras Summary: Presents methods for integrating RGB and depth data to improve object detection and spatial reasoning in indoor environments.

6. Object Detection: www.mdpi.com/1424-8220/24/9/2889: Paper: FusionVision: 3D Object Reconstruction with RGB-D Cameras Summary: Describes FusionVision, which combines RGB-D object detection and segmentation for precise 3D localization of objects.

