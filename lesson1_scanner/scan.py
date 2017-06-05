# Learning Open CV

# Import packages
from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filters import threshold_adaptive
import numpy as np 
import argparse
import cv2

# Arg parser construction
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to image to be scanned")
args = vars(ap.parse_args())

# Edge Detection
#Load the image, compute ratios of orig and new height

image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0 # Why 500?
orig = image.copy()
image = imutils.resize(image, height = 500)

# Image processing (grayscale)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray,(5,5),0)
edged = cv2.Canny(gray,75,200)

# Original image and edge detection
print "Step 1: Edge Detection"
cv2.imshow("Image",image)
cv2.imshow("Edged", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Step 2 - find the contours, keep only largest ones
# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
 
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
 
	# if our approximated contour has four points, then we
	# can assume that we have found our screen
	if len(approx) == 4:
		screenCnt = approx
		break
 
# show the contour (outline) of the piece of paper
print "STEP 2: Find contours of paper"
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
cv2.imshow("Outline", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Perspetive Transform

# 4 point transform
warped = four_point_transform(orig, screenCnt.reshape(4,2) * ratio)

# convert warped image to gray, threshold to give B/W paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
warped = threshold_adaptive(warped, 251, offset = 10)
warped = warped.astype("uint8") * 255

# Show images side by side
print "Step 3: Perspective Transform"
cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)


print 'end of script'