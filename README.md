# Head-pose controlled Robot
This Page showcases the working of the Head-pose controlled robot and the corresponding code.

![](https://github.com/tarunmadhira/Head-pose__controlled_Robot/blob/master/IMG_20191006_181805.jpg)

## Robot working demonstration 
![](https://github.com/tarunmadhira/Head-pose__controlled_Robot/blob/master/ezgif.com-video-to-gif.gif)

### What it does?

The robot moves accordning to head direction detected by the laptop webcam in real-time. 

The laptop webcam captures video frames and detects the user head-pose in each frame in terms of X, Y & Z coordinnates i.e pitch, rolll and yaw respectively. The head direction is then classified as up, down, left and right.

This head direction is the sent to robot for each frame. The robot is connected to the laptop over Wi-Fi. The robot moves forward when user is looking up, back when looking down, moves left when user looks left and moves right accordingly. All of this Happens in realtime, frame-by-frame. 

![Output of Head-pose tracking algorithm on laptop](https://github.com/tarunmadhira/Head-pose__controlled_Robot/blob/master/upload%20to%20git/headrit.png)

### How does it do it?

The system comprises of four steps as follows:

#### 1.) Face landmark detection

On capturing frame of video from laptop webcam, the first step is to calculate the 2D locations of 68 face landmark points. Face Landmark points are certain key points on face like tip of nose, cornner of eye etc. they are used to localize and label regions of the face. 

We employ a popular pre-trained model, the "Dlib shape predictor" ![](http://dlib.net/face_landmark_detection.py.html) 
It comprises of an HoG + Linear SVM based face detector combined with a sliding window technique and an image pyramid scheme. it uses an ensemble of regression tress to localize 2D locations of face landmrk points. it is based on the paper ![](http://openaccess.thecvf.com/content_cvpr_2014/html/Kazemi_One_Millisecond_Face_2014_CVPR_paper.html) 


#### 2.) Pose calculation 

The 3D head pose is calculated using the locations of 2D points captured by the dlib face landmark detector. We use the Orthographic projection techique to project the 2D landmark points to the corresponding 3D points. This method is reliable, accurate and fast, it is not as computationally intensive as the CNN & machine learning based approach.


