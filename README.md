# Head-pose controlled Robot
This Page showcases the Head-pose controlled robot and the corresponding code.

![](Head-pose__controlled_Robot/blob/master/IMG_20191006_181805.jpg)

## Robot working demonstration 
![GIF showing the Robot in action](https://github.com/tarunmadhira/Head-pose__controlled_Robot/blob/master/ezgif.com-video-to-gif.gif)

### What it does?

The robot moves according to head direction detected by the laptop webcam, in real-time. 

The laptop webcam captures video frames and detects the user head-pose in each frame in terms of X, Y & Z coordinates i.e pitch, roll and yaw respectively. The head direction is then classified as up, down, left and right.

This head direction is the sent to robot for each frame. The robot is connected to the laptop over Wi-Fi. The robot moves forward when user is looking up, back when looking down, moves left when user looks left and moves right accordingly. All of this happens in real-time, frame-by-frame. 

![Output of Head-pose tracking algorithm on laptop](https://github.com/tarunmadhira/Head-pose__controlled_Robot/blob/master/upload%20to%20git/headrit.png)

### How does it do it?

The system comprises of four steps:


#### 1.) Face landmark detection:

On capturing frame of video from laptop webcam, the first step is to calculate the 2D locations of 68 face landmark points. Face Landmark points are certain key points on the face like the tip of the nose, corner of eye etc. They are used to localize and label regions of the face. 

We employ a popular, fast & reliable pre-trained model, the "Dlib shape predictor" ![](http://dlib.net/face_landmark_detection.py.html) 
It comprises of an HoG + Linear SVM based face detector combined with a sliding window technique and an image pyramid scheme. It uses an ensemble of regression tress to localize 2D locations of face landmark points. Its working is based on the paper ![](http://openaccess.thecvf.com/content_cvpr_2014/html/Kazemi_One_Millisecond_Face_2014_CVPR_paper.html) 

It has been trained on the iBuG-300w Faces in-the-wild dataset ![](https://ibug.doc.ic.ac.uk/resources/300-W_IMAVIS/)


#### 2.) Pose calculation:

The 3D head pose is calculated using the locations of 2D points captured by the Dlib face landmark detector. We use the Orthographic projection techique to project the 2D landmark points to the corresponding 3D points. This method is reliable, accurate and fast, it is not as computationally intensive as the CNN & machine learning based approaches.

We use the POSiT( Pse from orthographic scaling with Iterations) algorithm for head-pose calculation. It transforms and projects 2D points to 3D. We supply it with the 2D landmark points from the Dlib face landmark detector, and we supply pre-defined camera calibration and distortion parameters. It also uses a generic 3D model for reference 3D points to calculate the rotation and translation vectors for the  projected 3D points with respect to the reference points of the head provided by the model. 
The generic 3D model refrence points are provided by ![](https://ibug.doc.ic.ac.uk/resources/300-W_IMAVIS/). The rotation and translation vectors gives the angles of pitch, yaw & roll i.e X, Y, & Z respectively. 

The POSiT algorith is implemented in python using the OpenCV function "Solve_PnP". It solves the 2D-3D correspondence equation using Direct Linear Transform followed by Levenberg-Marquardt optimization. ![](https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html) 

The diagram below illustrates Pitch, Yaw & Roll in terms of X, Y & Z

![](https://github.com/tarunmadhira/Head-pose__controlled_Robot/blob/master/upload%20to%20git/yawroll%26pitch.png)

#### 3.) Sending direction command:

The robot is connected to the Laptop wirelessly via Wi-Fi, the direction command being detected in the current frame (i.e up, down, left & right) is sent to robot in real time over TCP/IP. The data being sent is in string format. 

#### 4.) Motion executed:

If the word "up" is recieved, the robot moves forwards and so on as explained. The robot is controlled by a NodeMCU microcontroller IC, which drives an L293D motor driver IC. The IC in turn drives two motors. 

## The robot hardware 

The circuit diagram is as shown below ![](https://github.com/tarunmadhira/Head-pose__controlled_Robot/blob/master/upload%20to%20git/circuit.png)

The robot consists of NodeMCU microcontroller IC, two DC motors, an L293D motor driver IC and two 9v batteries for powerinng the NodeMCU and motors respectively. 

The NodeMCU (Node MicroController Unit) is an open source software and hardware development environment that is built around a very inexpensive System-on-a-Chip (SoC) called the ESP8266. The ESP8266, designed and manufactured by Espressif Systems, contains all crucial elements of the modern computer: CPU, RAM, networking (wifi), and even a modern operating system and SDK. When purchased at bulk, the ESP8266 chip costs only $2 USD a piece. That makes it an excellent choice for IoT projects of all kinds.

## Hardware & software used to run

* Intel i5 8th gen CPU
* 8 GB RAM
* Nvidia mx250 GPU 
* Windows 10 x86
* Python 3.6
* OpenCV 3 package
* Dlib 19.0 Python library
* iMutils Python library


#### How to run

* Download Dlib shape predictor pre-trained model "shape_predictor_68_face_landmarks.dat"
* Install OpenCV 3+ package, Dlib 19.0 library and the latest version of imutils. 
* flash the file "wificlientbasic2modded.ino" onto your NodeMCU (optional)
* Run "finalgui2.py" and switch on your NodeMCU if you want to conntrol robot after detecting headpose
* Run "finalgui2withoutserver.py" to run the head-pose detection algorithm ONLY, without a robot. 

##### CONTACT DETAILS-

Made by: Sai Tarun Madhira; MIT, Manipal, BTech. Electronics and communication engineering

Email- Saitarun.madhira@gmail.com

<video src="WhatsApp Video 2019-10-06 at 6.03.41 PM.mp4" width="320" height="200" controls preload></video>




