import math
import cv2
import easygui
import matplotlib.pyplot
import numpy as np
from matplotlib import pyplot as plt


def CreateHist(frame):
    # frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2YUV)

    Block = [Y,CR,CB] = cv2.split(frame)

    for i in  Block:
        values = i.ravel()
        # i = cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
        plt.hist(values,bins=256,range=[0,256], label=f'{i}')
        plt.show()


    return frame


T_state = "Binary"
T =  cv2.THRESH_TOZERO
TI = cv2.THRESH_TOZERO_INV

Y_Thresh_min = 0
Y_Thresh_max = 255
Cr_Thresh_min = 130
Cr_Thresh_max = 155
Cb_Thresh_min = 100
Cb_Thresh_max =  125

def echo_tresh():
    print("Y_min {}\nY_max {}\nU_min {}\nU_max {}\nV_min {}\nV_max {}".format(
        Y_Thresh_min,
        Y_Thresh_max,
        Cr_Thresh_min,
        Cr_Thresh_max,
        Cb_Thresh_min,
        Cb_Thresh_max
    ))

def set_threst_state(thresh_list):
    global T
    global TI

    
    thresh_list = thresh_list.split(" ")
    arg, *_ = thresh_list

    if(arg == "Binary"):
        # T =  cv2.THRESH_BINARY
        TI = cv2.THRESH_BINARY_INV
        return
    
    T =  cv2.THRESH_TOZERO
    TI = cv2.THRESH_TOZERO_INV



def set_Y_thresh(thresh_list):
    print(thresh_list)
    if(type(thresh_list)==str):
        thresh_list = thresh_list.split(" ")
        print(thresh_list)
        thresh_list = [eval(i) for i in thresh_list]
    

    global Y_Thresh_min
    global Y_Thresh_max
    
    Y_Thresh_min,Y_Thresh_max, *_ = thresh_list

def set_Cr_thresh(thresh_list):
    if(type(thresh_list)==str):
        thresh_list = thresh_list.split(" ")
        thresh_list = [eval(i) for i in thresh_list]

    global Cr_Thresh_min
    global Cr_Thresh_max
    
    Cr_Thresh_min,Cr_Thresh_max, *_ = thresh_list

def set_Cb_thresh(thresh_list):
    if(type(thresh_list)==str):
        thresh_list = thresh_list.split(" ")
        thresh_list = [eval(i) for i in thresh_list]

    global Cb_Thresh_min
    global Cb_Thresh_max
    
    Cb_Thresh_min,Cb_Thresh_max, *_ = thresh_list



def Isolate(frame):
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2YCrCb)

    Block = [Y,CR,CB] = cv2.split(frame)
    
    # resize down
    # CR = cv2.resize(CR,(0,0),fx=0.2, fy=0.2)
    # CB = cv2.resize(CB,(0,0),fx=0.2, fy=0.2)

    #YCrCb Thresholds for human skin
    cv2.threshold(Y,Y_Thresh_min,255,T, Y)
    cv2.threshold(Y,Y_Thresh_max,255,TI, Y)
    cv2.threshold(CR,Cr_Thresh_min,255,T, CR)
    cv2.threshold(CR,Cr_Thresh_max,255,TI,CR)
    cv2.threshold(CB,Cb_Thresh_min,255,T, CB)
    cv2.threshold(CB,Cb_Thresh_max,255,TI, CB)

    #Bitwise map for Cr Cb
    Processed_frame = cv2.bitwise_and(CR,CB)


    # Resize up and blur

    # CR = cv2.GaussianBlur(CR,(3,3),0.5)
    # CB = cv2.GaussianBlur(CB,(3,3),0.5)

    # CR = cv2.resize(CR,(0,0),fx=5, fy=5)
    # CB = cv2.resize(CB,(0,0),fx=5, fy=5)

    return Processed_frame, Y, CR, CB

def mask_stitch(Mask):

    #shape kernal
    shape = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

    # masks for opening and closing
    Mask_out = cv2.morphologyEx(Mask,cv2.MORPH_CLOSE,shape)
    Mask_out = cv2.morphologyEx(Mask,cv2.MORPH_OPEN,shape)


    return Mask_out