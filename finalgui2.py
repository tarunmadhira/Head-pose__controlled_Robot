# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 11:30:52 2019

@author: lenovo
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 16:57:19 2019

@author: lenovo
"""

import cv2
import dlib
import numpy as np
from imutils import face_utils
import socket


face_landmark_path = "F:\PycharmProjects\semGUI\shape_predictor_68_face_landmarks.dat"

K = [6.5308391993466671e+002, 0.0, 3.1950000000000000e+002,
     0.0, 6.5308391993466671e+002, 2.3950000000000000e+002,
     0.0, 0.0, 1.0]
D = [7.0834633684407095e-002, 6.9140193737175351e-002, 0.0, 0.0, -1.3073460323689292e+000]

cam_matrix = np.array(K).reshape(3, 3).astype(np.float32)
dist_coeffs = np.array(D).reshape(5, 1).astype(np.float32)

object_pts = np.float32([[6.825897, 6.760612, 4.402142],
                         [1.330353, 7.122144, 6.903745],
                         [-1.330353, 7.122144, 6.903745],
                         [-6.825897, 6.760612, 4.402142],
                         [5.311432, 5.485328, 3.987654],
                         [1.789930, 5.393625, 4.413414],
                         [-1.789930, 5.393625, 4.413414],
                         [-5.311432, 5.485328, 3.987654],
                         [2.005628, 1.409845, 6.165652],
                         [-2.005628, 1.409845, 6.165652],
                         [2.774015, -2.080775, 5.048531],
                         [-2.774015, -2.080775, 5.048531],
                         [0.000000, -3.116408, 6.097667],
                         [0.000000, -7.415691, 4.070434]])

reprojectsrc = np.float32([[10.0, 10.0, 10.0],
                           [10.0, 10.0, -10.0],
                           [10.0, -10.0, -10.0],
                           [10.0, -10.0, 10.0],
                           [-10.0, 10.0, 10.0],
                           [-10.0, 10.0, -10.0],
                           [-10.0, -10.0, -10.0],
                           [-10.0, -10.0, 10.0]])

line_pairs = [[0, 1], [1, 2], [2, 3], [3, 0],
              [4, 5], [5, 6], [6, 7], [7, 4],
              [0, 4], [1, 5], [2, 6], [3, 7]]


#def makeserver():




    #statusvar.set("unconnected ")


def setupServer():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind complete.")
    return s


def setupConnection():

    s.listen(1)  # Allows one connection at a time.
    conn, address = s.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    return conn


def get_head_pose(shape):
    image_pts = np.float32([shape[17], shape[21], shape[22], shape[26], shape[36],
                            shape[39], shape[42], shape[45], shape[31], shape[35],
                            shape[48], shape[54], shape[57], shape[8]])

    _, rotation_vec, translation_vec = cv2.solvePnP(object_pts, image_pts, cam_matrix, dist_coeffs)

    reprojectdst, _ = cv2.projectPoints(reprojectsrc, rotation_vec, translation_vec, cam_matrix,
                                        dist_coeffs)

    reprojectdst = tuple(map(tuple, reprojectdst.reshape(8, 2)))

    # calc euler angle
    rotation_mat, _ = cv2.Rodrigues(rotation_vec)
    pose_mat = cv2.hconcat((rotation_mat, translation_vec))
    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_mat)

    return reprojectdst, euler_angle


def headposecode():
    global command
    cap = cv2.imread('headpose.jpg')
    if (cap.all()==None):
        print("Unable to connect to load image.")
        return
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_landmark_path)
    frame=cap
    #while cap.isOpened():
        #ret, frame = cap.read()
        #if ret:
    face_rects = detector(frame, 0)

    if len(face_rects) > 0:
        shape = predictor(frame, face_rects[0])
        shape = face_utils.shape_to_np(shape)

        reprojectdst, euler_angle = get_head_pose(shape)

        for (x, y) in shape:
            cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        for start, end in line_pairs:
             cv2.line(frame, reprojectdst[start], reprojectdst[end], (0, 0, 255))

        cv2.putText(frame, "X: " + "{:7.2f}".format(euler_angle[0, 0]), (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 0, 0), thickness=2)
        cv2.putText(frame, "Y: " + "{:7.2f}".format(euler_angle[1, 0]), (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 0, 0), thickness=2)
        cv2.putText(frame, "Z: " + "{:7.2f}".format(euler_angle[2, 0]), (20, 120), cv2.FONT_HERSHEY_SIMPLEX,
                    0.75, (0, 0, 0), thickness=2)

        if (euler_angle[1, 0] > 25):
            cv2.putText(frame, "RIGHT", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), thickness=2)
            command = "right"
        elif (euler_angle[1, 0] < (-25)):
            cv2.putText(frame, "LEFT", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), thickness=2)
            command = "left"
        elif (((euler_angle[1, 0]) > (-25)) and (euler_angle[1, 0]) < (25) and ((euler_angle[0, 0]) < 0)):
            cv2.putText(frame, "UP", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), thickness=2)
            command = "forward"
        elif (((euler_angle[1, 0]) > (-40)) and (euler_angle[1, 0] < (40)) and (euler_angle[0, 0]) > (-15)):
            cv2.putText(frame, "DOWN", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), thickness=2)
            command = "backward"
    statusvar.set(command)
    cv2.imshow("demo", frame)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        #break
        cv2.destroyAllWindows()

###if __name__ == '__main__':
 #   main()

def sendcommand():
    print(command)
    conn.sendall(str.encode(command))
    data = conn.recv(1024)  # receive the data
    data = data.decode('utf-8')
        # Split the data such that you separate the command
        # from the rest of the data.
    dataMessage = data.split(' ', 1)
    c= dataMessage[0]
    reply=c.strip()
    print(reply)
    
    
def vidheadpose():
    # return
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Unable to connect to load footage.")
        return
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(face_landmark_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            face_rects = detector(frame, 0)

            if len(face_rects) > 0:
                shape = predictor(frame, face_rects[0])
                shape = face_utils.shape_to_np(shape)

                reprojectdst, euler_angle = get_head_pose(shape)

                for (x, y) in shape:
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

                for start, end in line_pairs:
                    cv2.line(frame, reprojectdst[start], reprojectdst[end], (0, 0, 255))

                cv2.putText(frame, "X: " + "{:7.2f}".format(euler_angle[0, 0]), (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 0), thickness=2)
                cv2.putText(frame, "Y: " + "{:7.2f}".format(euler_angle[1, 0]), (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 0), thickness=2)
                cv2.putText(frame, "Z: " + "{:7.2f}".format(euler_angle[2, 0]), (20, 120), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 0), thickness=2)
                
                if ((euler_angle[1,0]<15) and (euler_angle[1,0]>(-15))):
                    if((euler_angle[0,0]>0)):
                         cv2.putText(frame, "DOWN", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), thickness=2)
                         command="backward\n"
                    elif((euler_angle[0,0])<0):
                         cv2.putText(frame,"UP", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), thickness=2)
                         command="forward\n"
                elif(euler_angle[1,0]>15):
                     cv2.putText(frame,"RIGHT", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), thickness=2)
                     command="right\n"
                elif(euler_angle[1,0]<(-15)):
                     cv2.putText(frame, "LEFT", (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), thickness=2)
                     command="left\n"
                conn.sendall(str.encode(command))

            cv2.imshow("demo", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


def vidread():

    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    statusvar.set("OPENING LAST RECORDED FILE")
    cap = cv2.VideoCapture('outpy.avi')

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break
    statusvar.set("FINISHED PLAYING")
    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()


def vidsave():

    # Create a VideoCapture object
    statusvar.set("STARTING CAPTURE")
    cap = cv2.VideoCapture(0)
    frmno = int(entry1.get() or 0)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Unable to read camera feed")

    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 5, (frame_width, frame_height))

    while (frmno>0):
        ret, frame = cap.read()
        frmno = frmno - 1
        if ret == True:

            # Write the frame into the file 'output.avi'
            out.write(frame)

            # Display the resulting frame
            cv2.imshow('frame', frame)

            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break
            # When everything done, release the video capture and video write objects
    cap.release()
    out.release()

    # Closes all the frames
    statusvar.set("FINISHED CAPTURE outpy.avi")
    cv2.destroyAllWindows()


def preview():

    statusvar.set("STARTING CAMERA")
    cap = cv2.VideoCapture(0)
    frmno=int(entry1.get() or 0)
    #labelx = Label(window, image=a)

    while(cap.isOpened and frmno>0):
    # Capture frame-by-frame
        ret, frame = cap.read()
        frmno=frmno-1

    # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        #h,w,no=frame.shape
        #labelx.grid(coulumn=2, row=6)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    statusvar.set("FINISHED PREVIEW")
    cap.release()
    cv2.destroyAllWindows()

def headvideocode():
    #import linconhard2d3dpose
    os.system("python F:\PycharmProjects\semGUI\linconhard2d3dpose.py")
#def headimgcode():
    #os.system("python /Users/tarunmadhira/PycharmProjects/semGUI/orthoimage.py")
 #   os.system("python /Users/tarunmadhira/PycharmProjects/semGUI/leftrightpose.py")

#def headimgclientcode():
 #   os.system("python /Users/tarunmadhira/PycharmProjects/semGUI/leftrightcodeclient.py")

def imgcap():

    statusvar.set("STARTING CAMERA")
    cap = cv2.VideoCapture(0)

    for i in range(1):
    # Capture frame-by-frame
        ret, frame = cap.read()
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        #h,w,no=frame.shape
        #labelx.grid(coulumn=2, row=6)
        cv2.imwrite('headpose.jpg', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    statusvar.set("IMAGE CAPTURED")
    cap.release()
    cv2.destroyAllWindows()


def imgread():
    img=cv2.imread("headpose.jpg", 1)
    cv2.imshow('captured image', img)
    statusvar.set("SHOWING IMAGE")
    k= cv2.waitKey(0)
    if k == ord('q'):
        cv2.destroyAllWindows()


from tkinter import *
import os

window=Tk()
window.title("headpose robot command window")
statusvar=StringVar()
statusvar.set("GUI running")
label1=Label(window, text="press to begin live preview", font=100)
label1.grid(column=0, row=0)
label2=Label(window, text="enter total no. of frames")
label2.grid(column=2, row=1)
label3=Label(window, text="start recording for give no. of frames. 20fps")
label3.grid(column=0, row=2)
label4=Label(window, text="press to play video")
label4.grid(column=0, row=4)
label5=Label(window, text="press to run video code")
label5.grid(column=0, row= 6)
label6=Label(window, text="press to capture image ")
label6.grid(column=0, row= 8)
label7=Label(window, text="press to show captured image")
label7.grid(column=0, row= 10)
label8=Label(window, text="press to only run image code")
label8.grid(column=0, row= 12)
label9=Label(window, text="press to move")
label9.grid(column=0, row=14)
label10=Label(window, text="press to move in robot by head pose in real time")
label10.grid(column=0, row=16)

labela=Label(window, textvariable=statusvar, bg="green", relief= RAISED)
labela.grid(column=2, row=4)

entry1=Entry(window)
entry1.grid(column=2, row =2)

button1=Button(window, text="show preview", command=preview, fg="white", bg="blue")
button2=Button(window, text="record", command=vidsave, fg="white", bg="blue", activebackground="green",)
button3=Button(window, text="play saved video", command=vidread, fg="white", bg="blue")
button4=Button(window, text="run video code", command=headvideocode,fg="black", bg="blue" )
button5=Button(window, text="capture image", command=imgcap,fg="black", bg="red" )
button6=Button(window, text="show ", command=imgread, fg="black", bg="red")
button7=Button(window, text="see head orientation", command=headposecode,fg="black", bg="red")
button8=Button(window, text="send command & move", command=sendcommand, fg="black", bg="red")
button9=Button(window, text="full code", command=vidheadpose, fg="red", bg="green", highlightbackground="red")
#button10=Button(window, text="build server", command=makeserver, fg="black", bg="yellow")
button1.grid(column=0, row=1)
button2.grid(column=0, row=3)
button3.grid(column=0, row=5)
button4.grid(column=0, row=7)
button5.grid(column=0, row=9)
button6.grid(column=0,row=11)
button7.grid(column=0,row=13)
button8.grid(column=0,row=15)
button9.grid(column=0,row=17)
#button10.grid(column=2, row=4)







storedValue = "Yo, what's up?"
host = ''
port = 3001


s = setupServer()
conn=setupConnection()

window.geometry('700x700')
window.mainloop()



