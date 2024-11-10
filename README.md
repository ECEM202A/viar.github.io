# viar.github.io
Visually Impaired Accessible Room

## Project Idea: Smart Room System Using Depth Camera, Apple Watch, and Auditory Feedback for Blind Assistance 

Camera: Realsense L515 Lidar 

Contact: Jason Wu (jaysunwu@g.ucla.edu) 

## Overview:  
This project aims to provide visually impaired individuals with spatial awareness and navigational guidance using a combination of a depth camera, Apple Watch, and auditory feedback. The system helps users locate and retrieve objects with precise instructions, while the Apple Watch provides haptic feedback, and auditory cues offer real-time navigation and guidance.  
 

## Key Components: 
Depth Camera (RealSense L515): 
Provides a 3D map of the environment. 
Tracks the user's position and objects in the room. 
Identifies and localizes objects (e.g., phone, keys, wallet) with depth information, helping the system provide spatial guidance. 
https://www.jstage.jst.go.jp/article/jsp/23/4/23_201/_pdf/-char/en (Intel RealSense pathplanning) 
https://github.com/pancx/pathplanning + Intel® RealSense™ SLAM Library 
Apple Watch (Haptic Feedback): 
Delivers directional and spatial cues to guide the user towards the object. 
Different haptic patterns indicate directions (forward, left, right) or fine-tune movements for grasping objects. 
Provides feedback for both navigation and object retrieval. 
Auditory Spatial Feedback (Airpods/Headphones): 
Supplements haptic feedback with sound-based navigation cues. 
Audio cues vary in volume, pitch, or panning (left/right) to indicate direction, distance, and proximity to objects. 
Helps users build spatial awareness through a combination of sound and vibration, enabling finer control for object retrieval. 
Speech Recognition (Whisper OpenAI): 
Apple Speech to text: (https://developer.apple.com/tutorials/app-dev-training/transcribing-speech-to-text ) 
User issues voice commands like "Find my phone" or "Where is the table?" 
Speech recognition converts the command into actionable navigation instructions, processed by the depth camera and navigation system. 
Command Interpretation (Grok LLM): 
Processes user commands for complex tasks such as searching for specific objects or providing step-by-step navigation instructions. 
Offers context-aware feedback to guide users through detailed retrieval tasks. 
TCP communication between iOS app and Laptop  

## How It Works: 
### Room Scanning & Object Detection:  
The depth camera scans the room and detects objects, creating a real-time map of the environment. 
When the user requests an item, the system identifies its location and sends spatial information to both the Apple Watch and auditory feedback system. 
### Precise Navigation with Haptic and Auditory Feedback: 
<li>Haptic Feedback: 
The Apple Watch's haptic cues guide the user toward the object. A pattern of taps directs the user left, right, or forward. </li>
<li>Auditory Feedback: Sound cues complement haptic feedback by giving additional spatial information. For example, the sound may get louder or shift to the left or right as the user moves in the corresponding direction. </li>

### Accurate Spatial Instructions:
As the user approaches the object, the system provides precise spatial instructions through a combination of haptic and auditory feedback (e.g., text to speech, frequency changing, spatial audio, volume changing). 
The depth camera ensures that the user is accurately positioned to grasp the object. 
### Object Grasping & Feedback: 
The system, using object positioning data from the depth camera, gives final instructions via both haptic and auditory feedback to assist the user in accurately grasping the object. 
For instance, a vibration pattern could signal the final position for grasping, while an auditory cue might confirm the object’s proximity. 
 

## Current Apps on iOS: 

(List of apps from AppleVis which is a community of visually impaired people using apple tech) 

<li>Seeing AI: App by microsoft for voice instructions to users (using computer vision) </li>
<li>Autout: Spatial Feedback (https://www.applevis.com/apps/ios/navigation/autour) </li>
<li>LetSeeApp: Visual -> Audio feedback like SeeingAI (https://www.applevis.com/apps/ios/utilities/letseeapp) </li>
<li>Light Detector: Converts light that the camera receives into some particular frequency audio (https://www.applevis.com/apps/ios/utilities/light-detector) </li>
<li>BlindSquare: Outdoor navigation by voice description (https://www.applevis.com/apps/ios/navigation/blindsquare) </li>
<li>Cash Reader: Only app with haptic feedback, which tells you value of bill through vibrations (https://www.applevis.com/apps/ios/utilities/cash-reader-bill-identifier) </li>
 

## Supporting Research (Google Scholar): 
<ol>
 <li>Depth Cameras in Assistive Tech: Paper: "Using Depth Cameras for Object Detection and Navigation Assistance for the Visually Impaired" 
Discusses how depth cameras can map environments and aid in object detection and navigation. </li>
 <li>Haptic Feedback in Object Retrieval: Paper: "Haptic Feedback for Object Localization and Grasping in Assistive Technologies" 
Explores how haptic feedback can be used to guide users towards precise movements for object retrieval. 
</li>
 <li>Speech Recognition in Assistive Devices: Paper: "Speech Recognition Systems in Assistive Technologies: Navigating and Retrieving Objects" 
Reviews the use of voice-controlled systems for visually impaired navigation and object interaction. 
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9795125 
https://dl.acm.org/doi/abs/10.1145/2982142.2982160  </li>

<li>Moving Object Detection: www.mdpi.com/2313-433X/4/5/71: Paper: Moving Object Detection in RGBD Data 
Summary: Surveys background subtraction techniques for detecting moving objects using RGB-D cameras, highlighting the role of depth data in improving object detection accuracy. </li>

<li>Room Scanning: openaccess.thecvf.com/content_iccv_2013/papers/Lin_Holistic_Scene_Understanding_2013_ICCV_paper.pdf : Paper: Holistic Scene Understanding for 3D Object Detection with RGBD Cameras 
Summary: Presents methods for integrating RGB and depth data to improve object detection and spatial reasoning in indoor environments. </li>

<li>Object Detection: www.mdpi.com/1424-8220/24/9/2889: Paper: FusionVision: 3D Object Reconstruction with RGB-D Cameras 
Summary: Describes FusionVision, which combines RGB-D object detection and segmentation for precise 3D localization of objects. 
</li>

<li>
Microsoft Kinect: Uses depth cameras for real-time spatial awareness and could be adapted for blind navigation systems. 
OrCam MyEye: 
Provides wearable vision assistance through object detection and feedback, though without depth capabilities. 
</li>
</ol>



## Expected Outcome: 

A system that uses a depth camera to provide real-time, 3D navigation assistance. 
The Apple Watch delivers haptic cues, guiding users through spaces to locate and grasp objects with accuracy. 
Speech recognition allows hands-free control, and the system provides both directional navigation and fine-tuned object retrieval guidance. 

# Team Notes:
10/16 Notes 
Jason Vu –RealSense PHD guy 
 
