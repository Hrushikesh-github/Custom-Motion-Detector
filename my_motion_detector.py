'''
Usage python my_motion_detector.py --video path_to_video

A simple yet efficient motion detector can be made by comparing the variable path of the image with an fixed frame. 
However the method would fail in a non static environment (where the camera moves). The following code tries to overcome this and performs better than the simple motion detector but is not very efficient in a moving environment

The algorithm:
1. Loop over the frames of the video
2. Increase the contrast of the frame ( this step can be skipped in a good lighting but is better for underwater situations). Convert into grayscale(so that fps speed can be achieved) and blur to remove any noise. 
3. Two buffers are created, the motion buffer and background buffer. Motion buffer contains the 3 previous frames and the background frame contains 30 frames. The current frame is sent through the motion buffer and the pop out from the motion buffer goes to the background buffer. 
4. We take a weighted average of both the frames, obtain a absolute difference, apply a very small threshold and then dilate to remove any holes.
5. Contours are obtained and using cv2 we draw rectangles over the region. Non maximum suppression is used to suppress adjacent boxes.

The motion buffer is useful to detect even small movements and reference claims it even reduces noise. More weightage for newer frames is given. The more frames in the motion buffer, the higher the probability of detection, but the greater the error due to the inclusion of the “tail” of the moving object in the motion area.

Background buffer also reduces noise, it's average is like a short term static environment.

Note: This code works better if we need to detect an object moving with the camera fixed/slow moving as the difference is nothing but relative motion(the buffers help, but not completely). The motion of camera makes the surroundings also to be detected.
       A good example of this is the underwater video of 2 whales
      
      The weights have been lineraly distributed, we can try different combinations and also a lot of parameters can be tuned in the code 
      
'''
# import the necessary packages
import argparse
import imutils
import time
from collections import deque
import cv2
import numpy as np
from nms import non_max_suppression_fast

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min_area", type=int, default=1000, help="minimum area size")
ap.add_argument("-f", "--frame_rate", type=float, default=25, help="frame rate of given video")
ap.add_argument("-i", "--iterations", type=int, default=8, help="number of dilation iterations")
ap.add_argument("-o", "--overlap_thresh", type=float, default=0.2, help="threshold to consider for non maximum suppression b/w 0 to 1 ")
ap.add_argument("-m", "--motion", type=int, default=3, help="number of frames to be stored in motion buffer. For slow moving, increase it 3")
args = vars(ap.parse_args())

# intialize the buffers and weights
motion_buf = deque(maxlen=args["motion"])
bg_buf = deque(maxlen=30)

motion_weights = []
bg_weights = []

motion_weights = np.linspace(1, 0.1, args["motion"] - 1)
bg_weights = np.linspace(1, 0.1, 30)

# Capture the video and start looping through the frames and note the time which can be useful
if not args.get("video",False):
    camera = cv2.VideoCapture(0)

else:
    camera = cv2.VideoCapture(args["video"])

start_time = time.time()

while True:
    (grabbed,frame) = camera.read()
    loop_time = time.time()

    # If we failed to grab from cam or reached the end of the video, quit the loop
    if not grabbed :
        break

    # resize the frame, improve contrast in poor lightning, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    frame = cv2.convertScaleAbs(frame, alpha=1.3, beta=10)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_blur = cv2.GaussianBlur(gray, (21, 21), 0)

    # Ensure the buffers are filled in, otherwise numpy gives error calculating the average because weights are fixed
    motion_buf.appendleft(frame_blur)
    if len(motion_buf) < args["motion"]:
        continue

    bg_buf.appendleft(motion_buf.pop())
    if len(bg_buf) < 30:
        continue

    # Obtain the averages
    motion_avg = np.uint8(np.average(motion_buf, axis=0, weights=motion_weights))
    bg_avg = np.uint8(np.average(bg_buf, axis=0, weights=bg_weights))

    # compute the absolute difference between the averages and apply a low threshold to detect even the slightest of differences
    frameDelta = cv2.absdiff(bg_avg, motion_avg)
    thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contour on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=4)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Initalize boxes which stores rectangle coordinates and loop over the contours
    boxes = []
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
                continue

        # compute the bounding box for the contour, draw it on the frame,
        (x, y, w, h) = cv2.boundingRect(c)
        boxes.append(np.array([x, y, x+w, y+h],dtype="float"))

    # Apply non maximum suppression to remove any overlapping boxes and then draw on the frame
    pick = non_max_suppression_fast(np.array(boxes), overlapThresh=args["overlap_thresh"])
    for (x1, y1, x2, y2) in pick:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Ensure we go as per the frame rate
    end_time = time.time()
    while (end_time - loop_time) < 1 / args["frame_rate"]:
        end_time = time.time()

    # show the frame and record if the user presses a key
    cv2.imshow("Video", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
            break

# print the total time to ensure the video time is close to the operation time, if not we need to simplify the calculations.
total_time = time.time() - start_time
print(total_time)

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

