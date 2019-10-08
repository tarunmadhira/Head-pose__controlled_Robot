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

The system comprises of four steps; capturing frame of video and detecting face landmarks 

#### 1.) Face landmark detection

On capturing frame of video from laptop webcam, the first step is to calculate the 2D locations of 68 face landmark points. Face Landmark points are certain key points on face like tip of nose, cornner of eye etc. they are used to localize and label regions of the face. 

We employ a popular, fast & reliable pre-trained model, the "Dlib shape predictor" ![](http://dlib.net/face_landmark_detection.py.html) 
It comprises of an HoG + Linear SVM based face detector combined with a sliding window technique and an image pyramid scheme. it uses an ensemble of regression tress to localize 2D locations of face landmrk points. it is based on the paper ![](http://openaccess.thecvf.com/content_cvpr_2014/html/Kazemi_One_Millisecond_Face_2014_CVPR_paper.html) 

it has been trained on the iBuG-300w Faces in-the-wild dataset ![](https://ibug.doc.ic.ac.uk/resources/300-W_IMAVIS/)


#### 2.) Pose calculation 

The 3D head pose is calculated using the locations of 2D points captured by the dlib face landmark detector. We use the Orthographic projection techique to project the 2D landmark points to the corresponding 3D points. This method is reliable, accurate and fast, it is not as computationally intensive as the CNN & machine learning based approach.

We use the POSiT( Pse from orthographic scaling with Iterations) algorithm for head-pose calculation. It transforms and projects 2D points to 3D. We supply it with the 2D landmark points from the Dlib face landmark detector, and we supply pre-defined camera calibration and distration parameter. It also uses a generic 3D model for reference 3D points to calculate the rotation and translation vectors for the  projected 3D points. The generic 3D model refrence points are provided by ![](https://ibug.doc.ic.ac.uk/resources/300-W_IMAVIS/). The rotation and translation vectors gives the angles of pitch, yaw & roll i.e X, Y, & Z respectively. 

The POSiT algorith is implemented in python using the OpenCV function "Solve_PnP". It solves the 2D-3D correspondence equation using Direct Linear Transform followed by Levenberg-Marquardt optimization. ![](https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html) 

#### 3.) Sending direction command 

The robot is connected to the Laptop wirelessly via Wi-Fi, the direction command being detected in current frame (i.e up, down, left & right) is sent to robot in real time over TCP/IP. The data sent is in string format. 

#### 4.) Motion executed

If the word "up" is recieved the robot moves forwards and so on as explained. The robot is controlled by a NodeMCU microcontroller IC, which drives an L293D motor driver IC. The IC in turn drives two motors. 

## The robot hardware 

The circuit diagram is as shown below ![](https://github.com/tarunmadhira/Head-pose__controlled_Robot/blob/master/upload%20to%20git/circuit.png)

The robot consists of NodeMCU microcontroller IC, two DC motors, an L293D motor driver IC and two 9v batteries for powerinng the NodeMCU and motors respectively. 





