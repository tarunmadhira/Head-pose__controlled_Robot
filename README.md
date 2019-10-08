# Head-pose controlled Robot
This Page showcases the working of the Head-pose controlled robot and the corresponding code.

![](https://github.com/tarunmadhira/Head-pose__controlled_Robot/blob/master/IMG_20191006_181805.jpg)

## Robot working demonstration 
![](https://github.com/tarunmadhira/Head-pose__controlled_Robot/blob/master/ezgif.com-video-to-gif.gif)

### What it does?

The robot moves accordning to head direction detected by the laptop webcam in real-time. 

The laptop webcam captures video frames and detects the user head-pose in each frame in terms of X, Y & Z coordinnates i.e pitch, rolll and yaw respectively. The head direction is then classified as up, down, left and right.

This head direction is the sent to robot for each frame. The robot is connected to the laptop over Wi-Fi. The robot moves forward when user is looking up, back when looking down, moves left when user looks left and moves right accordingly. All of this Happens in realtime, frame-by-frame. 

![Output of Head-pose tracking algorithm on laptop]()

