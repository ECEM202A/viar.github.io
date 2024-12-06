## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import socket
import keyboard        
from tkinter import CURRENT
import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
import torch
from PIL import Image

import sys
sys.path.append('C:/Users/alexh/OneDrive/Desktop/UCLA Q1/ECE M202A/Project/VIAR/software')
print(sys.path)
from Pose.pose_landmark_pnp import *  # Now this works
className = "No Object"
UDP_IP = "131.179.20.99" 
UDP_PORT = 53
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

object3Dpoint = [0,0,0]
objectdepth = 0
min_distance = 0.01
max_distance = 8
drawline = 1
pose,ML = 1,2
Direction = "Wait"
alpha = 0.4 # exponential moving average smoothing factor
smoothed_head_angle = 0
smoothed_angle_object = 0

baseline_set = False


x,y = 0,0
prevObject3Dpoint = [0,0,0]
dpObject3Dpoint = 0,0,0
poseObject = init_pose(300,300)
model = torch.hub.load("yolov7", 'custom', 'yolov7.pt', source='local', force_reload=True) if ML == 2 else 0
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
            #print(label)
            drawline = 1
            cv2.circle(crop_img, (x,y), 10, (255, 255, 255), 2)#put circle midpoint of object
            objectmidpoint = x,y
            depth = get_depth(crop_img,depth_frame,x,y)
            objectdepth = "{:.2f}".format(depth)
     
            object3Dpoint = [objectmidpoint[0],objectmidpoint[1], objectdepth]
            cv2.putText(crop_img, label + str(object3Dpoint) , (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #print(str(object3Dpoint))

            return crop_img,object3Dpoint


def compute_hand_object_magnitude(x_wrist, y_wrist, handdepth, object3Dpoint, depth_scale):

    handdepth = float(handdepth)
    handdepth /= depth_scale

    # Normalize z to match x,y scale
    normalized_z = float(object3Dpoint[2]) / depth_scale

    # Compute the hand-to-object vector
    hand_to_object_vector = np.array([
        object3Dpoint[0] - x_wrist, 
        object3Dpoint[1] - y_wrist,  
        normalized_z - handdepth     
    ])

    # Compute the magnitude euclidian distance
    magnitude = np.linalg.norm(hand_to_object_vector)
    return magnitude
               

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

#UDP setup
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#server_address = ('localhost', 10000)
#sock.bind(server_address)
#sock.setblocking(False)



depth_sensor.set_option(rs.option.min_distance, min_distance)  # Set minimum distance


found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30) #enable 640x480 color 
config.enable_stream(rs.stream.depth, 320, 240, rs.format.z16, 30)#enable 320x240 depth

# Start streaming
pipeline.start(config)

try:
    while True:

        #UDP TEST
        # Receive data from the client
        try:
            # Attempt to receive data
            
            MESSAGE = f"{Direction}"
            sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
            #print(f"Sent: {MESSAGE} to {UDP_IP}:{UDP_PORT}")
            #print(f"Received {len(data)} bytes from {address}: {data.decode('utf-8')}")
        except BlockingIOError:
        # Handle cases where no data is available
            #print("No data available, continuing...")
            if(0):
                print("no data received")


        # Send a response back to the client

        #UDP TEST

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
            resized_image = cv2.resize(color_image, dsize = (300,300), interpolation=cv2.INTER_AREA)# (round(expected * aspect), expected)) #resize image to 300x300 for ML model
            #resized_depthmap = cv2.resize(depth_image, (round(expected * aspect), expected))
            #crop_start = round(expected * (aspect - 1) / 2)
            crop_img = resized_image#[0:expected, crop_start:crop_start+expected]
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
                #print(detections.shape)
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
            if(ML == 2) and keyboard.is_pressed('a') :#reset object position
               crop_img,object3Dpoint =  findObject(crop_img,depth_image,"bottle")
               #cv2.putText(crop_img, className,(int(xmin * expected), int(ymin * expected) - 5),cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255))
               prevObject3Dpoint = int(object3Dpoint[0]*640/300),int(object3Dpoint[1]*480/300), object3Dpoint[2] #prevObject3D takes 3D point and converts to color frame pixels
               dpObject3Dpoint= rs.rs2_deproject_pixel_to_point(intrinsics, (prevObject3Dpoint[0],prevObject3Dpoint[1]), float(prevObject3Dpoint[2]))
               dpObject3Dpoint = tuple(round(value, 2) for value in dpObject3Dpoint)

               baseline_set = False

               crop_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)
            else:#use previous object point to draw circle
                cv2.circle(crop_img, (object3Dpoint[0], object3Dpoint[1]), 10, (0, 255, 0), -1)  # Draw a green circle for the right wrist
                #cv2.circle(depth_colormap, (int(object3Dpoint[0]*640/300), int(object3Dpoint[1]*480/300)), 10, (0, 255, 0), -1)  # Draw a green circle for the right wrist

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
           [annotated_image,x_wrist,y_wrist,x_nose_original,y_nose_original,forward_vector,head_angle] = draw_pose(crop_img,poseObject)
           
           previousHandDepth = get_depth(annotated_image,depth_image,x_wrist,y_wrist)
           previousNoseDepth = get_depth(annotated_image,depth_image,x_nose_original,y_nose_original)

           x_wrist = int(x_wrist/300*640)
           y_wrist =int(y_wrist/300*480)

           x_nose = int(x_nose_original/300*640.0)
           y_nose =int(y_nose_original/300*480.0)

           annotated_image = cv2.resize(annotated_image, dsize = (640,480), interpolation=cv2.INTER_AREA)

           angle_object = 361


           cv2.circle(annotated_image, (x_nose, y_nose), 2, (0, 0, 255), -1)


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


        if(x_nose!=0 and y_nose!=0 and x_nose<=640 and y_nose<=480):
            depth_x = x_nose
            depth_y = y_nose

            #print(depth_x, depth_y)

            cv2.circle(depth_colormap, (depth_x, depth_y), 10, (0, 255, 0), -1)  # Draw a green circle for the nose

            nose_position = [x_nose, y_nose]

            #print("previous nosedepth = " + str(previousNoseDepth))
            nosedepth = get_depth(annotated_image, depth_image, x_nose, y_nose)
            #print("current nosedepth at " + str(x) + ", " + str(y) + " = " + str(nosedepth) )

            if(x_nose<=640 and y_nose <= 480):# and (nosedepth > 0 )):
                previousNoseDepth = nosedepth
                nose3Dpoint = [x_nose, y_nose, nosedepth]
                nosedepth = "{:.2f}".format(nosedepth)
                if(drawline == 1):
                # drawline = 0
                    #print("drawing line")
                    annotated_image = cv2.line(annotated_image, (nose3Dpoint[0], nose3Dpoint[1]), (prevObject3Dpoint[0], prevObject3Dpoint[1]), (255,0,0))

                #print(str(nose_position) + "," + nosedepth)
                dpNose3Dpoint = rs.rs2_deproject_pixel_to_point(intrinsics, (nose3Dpoint[0], nose3Dpoint[1]), float(nose3Dpoint[2]))
                dpNose3Dpoint = tuple(round(value, 2) for value in dpNose3Dpoint)

                cv2.putText(
                            annotated_image, str(dpNose3Dpoint[0]) + "," + str(dpNose3Dpoint[1]) + "," + str(dpNose3Dpoint[2]) + "meters", (x_nose, y_nose), 
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=0.4, 
                            color=(255, 0, 0), 
                            thickness=1, 
                            lineType=cv2.LINE_AA
                    )
                
                # Convert tuples to NumPy arrays
                dpNose3Dpoint = np.array(dpNose3Dpoint)
                dpObject3Dpoint = np.array(dpObject3Dpoint) 

                # Calculate nose to object vector
                head_to_object_vector = dpObject3Dpoint - dpNose3Dpoint

                # Calculate the nose-object angle
                angle_object = np.degrees(np.arctan2(head_to_object_vector[0], head_to_object_vector[2]))
                angle_object += 180
                if angle_object < 0:
                    angle_object += 360

                # Exponential moving average smoothing for both angle values
                smoothed_head_angle = alpha * head_angle + (1 - alpha) * smoothed_head_angle
                smoothed_angle_object = alpha * angle_object + (1 - alpha) * smoothed_angle_object

                """                 if abs(smoothed_head_angle - smoothed_angle_object) < 20:
                                    Direction = "Forward"
                                    print("Forward")
                                elif smoothed_head_angle < smoothed_angle_object - 20:
                                    Direction = "Right"

                                    print("Right")
                                elif smoothed_head_angle > smoothed_angle_object + 20:
                                    Direction = "Left"
                                    print("Left")
                                else:
                                    print("??") """

                #print(f"deprojected x {nose3Dpoint[0]}", f"x_nose: {x_nose}")

        if(x_wrist!=0 and y_wrist!=0 and x_wrist<=640 and y_wrist<=480):
            depth_x = x_wrist
            depth_y = y_wrist
            #print(" pose = " + str(x) + ", " + str(y) + " depth = " + str(depth_x) + "," + str(depth_y) )
            cv2.circle(depth_colormap, (depth_x, depth_y), 10, (0, 255, 0), -1)  # Draw a green circle for the right wrist



            hand_position = [x_wrist,y_wrist]

            
            #print("previous handdepth = " + str(previousHandDepth))
            handdepth = get_depth(annotated_image,depth_image,x_wrist,y_wrist)
            #print("current handdepth at " + str(x) + ", " + str(y) + " = " + str(handdepth) )



            if(x_wrist<640 and y_wrist < 480 and (handdepth > 0 )):
                previousHandDepth = handdepth
                hand3Dpoint = [x_wrist,y_wrist,handdepth]
                handdepth = "{:.2f}".format(handdepth)
                if(drawline == 1):
                   # drawline = 0
                    #print("drawing line")
                    annotated_image = cv2.line(annotated_image, (hand3Dpoint[0],hand3Dpoint[1]), (prevObject3Dpoint[0],prevObject3Dpoint[1]), (255,0,0))

                #print(str(hand_position) + "," + handdepth)
                dpHand3Dpoint= rs.rs2_deproject_pixel_to_point(intrinsics, (hand3Dpoint[0],hand3Dpoint[1]), float(hand3Dpoint[2]))
                dpHand3Dpoint = tuple(round(value, 2) for value in dpHand3Dpoint)

                if baseline_set is False:
                    baseline_hand_object_mag = compute_hand_object_magnitude(x_wrist, y_wrist, handdepth, object3Dpoint, depth_scale)
                    baseline_set = True

                hand_object_mag = compute_hand_object_magnitude(x_wrist, y_wrist, handdepth, object3Dpoint, depth_scale)

                #percent_change = (1/(hand_object_mag / baseline_hand_object_mag)) * 100

                test = 1 + (hand_object_mag - 1) * (100 - 1) / (1.25*baseline_hand_object_mag - 1)
            
                print(f"Mapping: {test}", f"Original: {hand_object_mag}", f"Baseline{baseline_hand_object_mag}")

                cv2.putText(
                            annotated_image, str(dpHand3Dpoint[0]) + "," + str(dpHand3Dpoint[1]) + "," + str(dpHand3Dpoint[2]) + "meters", (x_wrist, y_wrist), 
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=0.4, 
                            color=(255, 0, 0), 
                            thickness=1, 
                            lineType=cv2.LINE_AA

                    )
                dpHand3Dpoint - dpObject3Dpoint
                #print(className + "  Object 3D point = " + str(object3Dpoint))
                #print("Object 3D deprojected Point = " + str(dpObject3Dpoint))

                #print("Hand 3D point = " + str(hand3Dpoint))
                #print("Hand 3D deprojected Point = " + str(dpHand3Dpoint))


                """                 x_wrist = float(x_wrist)  # Convert to float if necessary
                                y_wrist = float(y_wrist)  # Convert to float if necessary
                                handdepth = float(handdepth)  # Convert depth to float

                                # Normalize x, y coordinates using depth to align scales
                                real_world_hand_3D = np.array([
                                    (x_wrist - intrinsics.ppx) * handdepth / intrinsics.fx,  # Convert x from pixels to meters
                                    (y_wrist - intrinsics.ppy) * handdepth / intrinsics.fy,  # Convert y from pixels to meters
                                    handdepth  # z (depth) remains the same
                                ])

                                real_world_object_3D = np.array([
                                    (object3Dpoint[0] - intrinsics.ppx) * float(object3Dpoint[2]) / intrinsics.fx,  # Convert x from pixels to meters
                                    (object3Dpoint[1] - intrinsics.ppy) * float(object3Dpoint[2]) / intrinsics.fy,  # Convert y from pixels to meters
                                    float(object3Dpoint[2])  # z (depth) remains the same
                                ]) """
                

                
        #print(f"Head Angle: {smoothed_head_angle}", f"Head-object Angle: {smoothed_angle_object}")
        
        if depth_colormap_dim != annotated_image.shape:
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



