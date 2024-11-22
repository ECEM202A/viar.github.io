## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2
import sys
sys.path.append('C:/Users/User/Source/Repos/viar.github.io')
print(sys.path)
from Pose.pose import *  # Now this works
className = "No Object"
object3Dpoint = [0,0,0]
objectdepth = 0
min_distance = 0.01
max_distance = 8
ML = 1
previousHandDepth  = handdepth = 9.0
#Configure pose detection
MODEL_PATH = os.path.expanduser('../Pose/pose_landmarker_full.task')
# Init PoseLandmarker
detector = initialize_pose_landmarker()

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))
depth_sensor = pipeline_profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()



depth_sensor.set_option(rs.option.min_distance, min_distance)  # Set minimum distance


found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 320, 240, rs.format.z16, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        align = rs.align(rs.stream.color)
        frames = align.process(frames)
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        profile = depth_frame.profile
        intrinsics = profile.as_video_stream_profile().get_intrinsics()

        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        
        

        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.01), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))



         # Standard OpenCV boilerplate for running the net:
         
            height, width = color_image.shape[:2]
            expected = 227
            aspect = width / height
            resized_image = cv2.resize(color_image, (round(expected * aspect), expected))
            crop_start = round(expected * (aspect - 1) / 2)
            crop_img = resized_image[0:expected, crop_start:crop_start+expected]
            if( ML == 1): #set ML to 1 for classifier bounding box from mobilenetSSD
                net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt", "MobileNetSSD_deploy.caffemodel")
                inScaleFactor = 0.007843
                meanVal       = 127.53
                classNames = ("background", "aeroplane", "bicycle", "bird", "boat",
                              "bottle", "bus", "car", "cat", "chair",
                              "cow", "diningtable", "dog", "horse",
                              "motorbike", "person", "pottedplant",
                              "sheep", "sofa", "train", "tvmonitor")

                blob = cv2.dnn.blobFromImage(crop_img, inScaleFactor, (expected, expected), meanVal, False)
                net.setInput(blob, "data")
                detections = net.forward()
                print(detections.shape)
                label = detections[0,0,0,1]
                conf  = detections[0,0,0,2]
                xmin  = detections[0,0,0,3]
                ymin  = detections[0,0,0,4]
                xmax  = detections[0,0,0,5]
                ymax  = detections[0,0,0,6]

                className = classNames[int(label)]
                if(className != "person"):

                    cv2.rectangle(crop_img, (int(xmin * expected), int(ymin * expected)), 
                                 (int(xmax * expected), int(ymax * expected)), (255, 255, 255), 2)
                    cv2.putText(crop_img, className, 
                                (int(xmin * expected), int(ymin * expected) - 5),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255))
             
                    objectmidpoint = (int(((xmax + xmin)/2) * expected),int(((ymax + ymin)/2) * expected))
                    objectdepth = depth_image[objectmidpoint].astype(float)
                    objectdepth = "{:.2f}".format(objectdepth * depth_scale)
     
                    cv2.putText(crop_img,str(objectmidpoint) + str(objectdepth) + "meters",objectmidpoint,cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255))
                    object3Dpoint = [objectmidpoint[0],objectmidpoint[1], objectdepth]


        type(crop_img)
        #pose detection
        detection_result = detect_pose_landmarks_from_array(crop_img, detector)
        annotated_image = draw_landmarks_on_image(crop_img, detection_result)
        #hand position data
        hand_position = [160,120]
        #hand_position = get_hand_position()
        x = hand_position[0]
        y = hand_position[1]
        print("previous handdepth = " + str(previousHandDepth))
        print("current handdepth = " + str(depth_image[hand_position].astype(float) * depth_scale))
        if(hand_position[0]<320 and hand_position[1] < 240 and (depth_image[hand_position].astype(float) > 0 and (depth_image[hand_position].astype(float) * depth_scale < (float(previousHandDepth)+ 1.0)))):
            previousHandDepth = handdepth
            handdepth = depth_image[hand_position].astype(float)
            handdepth = "{:.2f}".format(handdepth * depth_scale)


            print(str(get_hand_position()) + "," + handdepth)
            cv2.putText(
                        annotated_image, str(x) + "," + str(y) + "," +handdepth + "meters", (x, y), 
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                        fontScale=0.4, 
                        color=(255, 0, 0), 
                        thickness=1, 
                        lineType=cv2.LINE_AA

                )
            hand3Dpoint = {x,y,handdepth}
            dpObject3Dpoint= rs.rs2_deproject_pixel_to_point(intrinsics, [object3Dpoint[0],object3Dpoint[1]], float(objectdepth))
            print(className + "  Object 3D point = " + str(object3Dpoint))
            print("Object 3D deprojected Point = " + str(dpObject3Dpoint))

            print("Hand 3D point = " + str(hand3Dpoint))
            dpHand3Dpoint= rs.rs2_deproject_pixel_to_point(intrinsics, [x,y], float(handdepth))
            print("Hand 3D deprojected Point = " + str(dpHand3Dpoint))


        if depth_colormap_dim != color_colormap_dim or 1:
             
            resized_color_image = cv2.resize(annotated_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((annotated_image, depth_colormap))
            
       



        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()