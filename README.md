# Custom-Motion-Detector
I created a custom motion detector which draws a bounding box when any motion is detected. 
The main algorithm is taking the difference between frames in a video;
few major differences I made from other motion detector algorithms are: 
Using motion and background buffers of different sizes which are averaged with the newly added 
frames having more weightage and taking the difference of that averages, applying non-maximum suppression 
to suppress boxes detecting same motion and applying morphological transformations which yield a better result.  
