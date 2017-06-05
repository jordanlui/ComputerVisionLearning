import cv2
import time
# import imutils
cap = cv2.VideoCapture("test1.mp4")
# cap = cv2.VideoCapture("test2.mp4")
cap = cv2.VideoCapture(0) # This should capture from the webcam
print cap.isOpened()   # True = read video successfully. False - fail to read video.

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output_video.avi", fourcc, 20.0, (640, 480))
print out.isOpened()  # True = write out video successfully. False - fail to write out video.


(grabbed, frame) = cap.read()
# frame = imutils.resize(frame, width=600)
cv2.imshow("Frame", frame)
print frame.shape

time.sleep(5)
cap.release()
out.release()
