# -*- coding: utf-8 -*-
"""
Created on Thu Jun 08 14:32:14 2017

@author: Jordan
OpenCV Learning Series - Skin Tracking

Run the script and it will access your webcam
Otherwise, supply a video link to it
python skindetector.py --video video/skin_example.mov
python skindetector.py
"""
from pyimagesearch import imutils
import numpy as np
import argparse, cv2

# Arg parse
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to vid file. optional")
args = vars(ap.parse_args())

# Upper and lower colour bounds (HSV space)
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

# Grab webcam video unless we supply a video link
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
    
    #otherwise load the video
else:
    camera = cv2.VideoCapture(args["video"])
    
# Read video frames from our video / webcam

while True:
    # Grab vid frame
    (grabbed, frame) = camera.read()
    
    # If we are viewing video and don't get frame, we have reached end
    if args.get("video") and not grabbed:
        break
    
    # Resize frame, color processing and do masking based on our thresholds
    # Created mask will be white (255) for skin areas, and black for non skin areas
    frame = imutils.resize(frame,width = 400)
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    
    # Erosions and dilations to mask (softening)
    # Elliptical structuring kernel. Kernel and processing help remove false positives
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    
    # blur to remove noise, apply mask
    skinMask = cv2.GaussianBlur(skinMask, (3,3),0)
    skin = cv2.bitwise_and(frame,frame,mask = skinMask)
    
    # Show the skin in the image along with the mask
    cv2.imshow("iamges", np.hstack([frame,skin]))
    
    # Break loop if we hit 'q'
    if cv2.waitKey(1) and 0xFF == ord("q"):
        break
    
# Clean up 
camera.release()
cv2.destroyAllWindows()