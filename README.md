# Custom-Motion-Detector
I created a custom motion detector which draws a bounding box when any motion is detected. 

The main algorithm is taking the difference between frames in a video. Few major differences I made from other motion detector algorithms are: 

Using motion and background buffers of different sizes which are averaged with the newly added frames having more weightage and taking the difference of that averages, applying non-maximum suppression to suppress boxes detecting same motion and applying morphological transformations which yield a better result.  

There are a number of tunable parameters and a default has been set with a lot of experimenting. 

![hope2](https://user-images.githubusercontent.com/56476887/94722244-a5f02300-0374-11eb-826c-fbc6dccc1cb0.gif)



