# Custom-Motion-Detector
I created a custom motion detector which draws a bounding box when any motion is detected. 

Using motion and background buffers of different sizes which are averaged with the newly added frames having more weightage and taking the difference of that averages, applying non-maximum suppression to suppress boxes detecting same motion and applying morphological transformations which yield a better result.  

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

There are a number of tunable parameters and a default has been set with a lot of experimenting. 

# Results

![hope2](https://user-images.githubusercontent.com/56476887/94722244-a5f02300-0374-11eb-826c-fbc6dccc1cb0.gif)

![birds](https://user-images.githubusercontent.com/56476887/94723448-662a3b00-0376-11eb-9e86-4d330d521040.gif)




