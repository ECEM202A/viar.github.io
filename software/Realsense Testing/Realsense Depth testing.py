## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

def get_depth(rgb_image,depth_image,x,y):
# Get dimensions of both images
    rgb_height, rgb_width, _ = rgb_image.shape
    depth_height, depth_width = depth_image.shape

    # Scale the (x, y) coordinates for the depth image if sizes differ
    depth_x = int(x * (depth_width / rgb_width))
    depth_y = int(y * (depth_height / rgb_height))

    # Clamp the scaled coordinates to be within valid bounds
    depth_x = min(max(depth_x, 0), depth_width - 1)
    depth_y = min(max(depth_y, 0), depth_height - 1)

    # Retrieve RGB values and depth value
    depth_value = depth_image[depth_y, depth_x] * depth_scale

    return depth_value

def findObject(frame,depth_frame,objectName):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    crop_img = frame
    #crop_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    image_pil = Image.fromarray(crop_img)  # Convert to PIL Image
    results = model(image_pil)
    detections = results.xyxy[0]  # Bounding box coordinates, confidence, and class
    for det in detections:
        x1, y1, x2, y2, conf, cls = map(int, det[:6])
        label = f"{className[int(cls)]}: {conf:.2f}"
        x = int((x1 + x2 )/2)
        y = int((y1 +y2) /2)
        if(className[int(cls)] == objectName):
        # Draw bounding box and label
            print(label)
            drawline = 1
            cv2.circle(crop_img, (x,y), 10, (255, 255, 255), 2)#put circle midpoint of object
            objectmidpoint = x,y
            depth = get_depth(crop_img,depth_frame,x,y)
            objectdepth = "{:.2f}".format(depth)
     
            object3Dpoint = [objectmidpoint[0],objectmidpoint[1], objectdepth]
            cv2.putText(crop_img, label + str(object3Dpoint) , (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print(str(object3Dpoint))

            return crop_img,object3Dpoint
               

import keyboard        
from tkinter import CURRENT
import pyrealsense2 as rs
import numpy as np
import cv2
import torch
from PIL import Image
import sys
sys.path.append('C:/Users/User/Source/Repos/viar.github.io/software')
print(sys.path)
from Pose.pose_landmark_pnp import *  # Now this works
className = "No Object"
object3Dpoint = [0,0,0]
objectdepth = 0
min_distance = 0.01
max_distance = 8
drawline = 1
pose,ML = 1,2
x,y = 0,0
prevObject3Dpoint = [0,0,0]
dpObject3Dpoint = 0,0,0
poseObject = init_pose(300,300)
model = torch.hub.load("software/yolov7", 'custom', 'software/yolov7.pt', source='local', force_reload=False) if ML == 2 else 0
className =  ('person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush' )

previousHandDepth  = handdepth = 9.0
#Configure pose detection
#MODEL_PATH = os.path.expanduser('../Pose/pose_landmarker_full.task')
# Init PoseLandmarker

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
            expected = 300
            aspect = width / height
            resized_image = cv2.resize(color_image, (round(expected * aspect), expected))
            #resized_depthmap = cv2.resize(depth_image, (round(expected * aspect), expected))
            crop_start = round(expected * (aspect - 1) / 2)
            crop_img = resized_image[0:expected, crop_start:crop_start+expected]
            #depth_image = resized_depthmap[0:expected, crop_start:crop_start+expected]
            if( ML == 1): #set ML to 1 for classifier bounding box from mobilenetSSD
                net = cv2.dnn.readNetFromCaffe("C:/Users/User/Source/Repos/viar.github.io/software/MobileNetSSD_deploy.prototxt", "C:/Users/User/Source/Repos/viar.github.io/software/MobileNetSSD_deploy.caffemodel")
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
                if(className != "person" and className == "bottle"):
                    drawline = 1
                    cv2.circle(crop_img, (int((xmax + xmin) * expected/2), int((ymax + ymin) * expected/2)), 10, (255, 255, 255), 2)#put circle midpoint of object
                    #cv2.putText(crop_img, className, 
                     #           (int(xmin * expected), int(ymin * expected) - 5),
                      #          cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255))
             
                    objectmidpoint = (int(((xmax + xmin)/2) * expected),int(((ymax + ymin)/2) * expected))
                    objectdepth = depth_image[objectmidpoint].astype(float)
                    objectdepth = "{:.2f}".format(objectdepth * depth_scale)
     
                    #cv2.putText(crop_img,str(objectmidpoint) + str(objectdepth) + "meters",objectmidpoint,cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255))
                    object3Dpoint = [objectmidpoint[0],objectmidpoint[1], objectdepth]
            if(ML == 2 and keyboard.is_pressed('a') ):
               crop_img,object3Dpoint =  findObject(crop_img,depth_image,"bottle")
                    #cv2.putText(crop_img, className, 
                     #           (int(xmin * expected), int(ymin * expected) - 5),
                      #          cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255))
               prevObject3Dpoint = int(object3Dpoint[0]*640/300),int(object3Dpoint[1]*480/300), object3Dpoint[2]
               dpObject3Dpoint= rs.rs2_deproject_pixel_to_point(intrinsics, (prevObject3Dpoint[0],prevObject3Dpoint[1]), float(prevObject3Dpoint[2]))
               dpObject3Dpoint = tuple(round(value, 2) for value in dpObject3Dpoint)

               crop_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)
            else:
                cv2.circle(crop_img, (object3Dpoint[0], object3Dpoint[1]), 10, (0, 255, 0), -1)  # Draw a green circle for the right wrist
                
                cv2.putText(
                            crop_img, str(dpObject3Dpoint[0]) + "," + str(dpObject3Dpoint[1]) + "," + str(dpObject3Dpoint[2]) + "meters", (object3Dpoint[0],object3Dpoint[1]), 
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=0.4, 
                            color=(255, 0, 0), 
                            thickness=1, 
                            lineType=cv2.LINE_AA

                    )

                 




        #pose detection
        #hand position data
        #hand_position = {160,120}
        if(pose == 1):
           [annotated_image,x,y] = draw_pose(crop_img,poseObject)
           previousHandDepth = get_depth(annotated_image,depth_image,x,y)
           x = int(x/300*640)
           y=int(y/300*480)
           annotated_image = cv2.resize(annotated_image, dsize = (640,480), interpolation=cv2.INTER_AREA)
           

           #cv2.putText(
            #                annotated_image, str(x) + "," + str(y) + "," + str(previousHandDepth) + "meters", (int(x), int(y)), 
             #               fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
              #              fontScale=0.4, 
               #             color=(255, 0, 0), 
                #            thickness=1, 
                 #           lineType=cv2.LINE_AA

                  #  )

        else:
            annotated_image = crop_img
        if(x!=0 and y!=0 and x<=640 and y<=480):
            depth_x = x
            depth_y = y
            print(" pose = " + str(x) + ", " + str(y) + " depth = " + str(depth_x) + "," + str(depth_y) )
            cv2.circle(depth_colormap, (depth_x, depth_y), 10, (0, 255, 0), -1)  # Draw a green circle for the right wrist



            hand_position = [x,y]

            
            print("previous handdepth = " + str(previousHandDepth))
            handdepth =get_depth(annotated_image,depth_image,x,y)
            print("current handdepth at " + str(x) + ", " + str(y) + " = " + str(handdepth) )


            if(x<480 and y < 640 and (handdepth > 0 )):
                previousHandDepth = handdepth
                hand3Dpoint = [x,y,handdepth]
                handdepth = "{:.2f}".format(handdepth)
                if(drawline == 1):
                   # drawline = 0
                    print("drawing line")
                    annotated_image = cv2.line(annotated_image, (hand3Dpoint[0],hand3Dpoint[1]), (prevObject3Dpoint[0],prevObject3Dpoint[1]), (255,0,0))

                print(str(hand_position) + "," + handdepth)
                dpHand3Dpoint= rs.rs2_deproject_pixel_to_point(intrinsics, (hand3Dpoint[0],hand3Dpoint[1]), float(hand3Dpoint[2]))
                dpHand3Dpoint = tuple(round(value, 2) for value in dpHand3Dpoint)

                cv2.putText(
                            annotated_image, str(dpHand3Dpoint[0]) + "," + str(dpHand3Dpoint[1]) + "," + str(dpHand3Dpoint[2]) + "meters", (x, y), 
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=0.4, 
                            color=(255, 0, 0), 
                            thickness=1, 
                            lineType=cv2.LINE_AA

                    )
                
                #print(className + "  Object 3D point = " + str(object3Dpoint))
                #print("Object 3D deprojected Point = " + str(dpObject3Dpoint))

                #print("Hand 3D point = " + str(hand3Dpoint))
                #print("Hand 3D deprojected Point = " + str(dpHand3Dpoint))


        if depth_colormap_dim != color_colormap_dim or 1:
            resized_color_image = cv2.resize(annotated_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((annotated_image, depth_colormap))
            
       

       #images = cv2.resize(images, (1280,720))


        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow('RealSense', resized_color_image)

        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()



