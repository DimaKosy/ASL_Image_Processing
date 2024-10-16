import math
import cv2
import easygui
import matplotlib.pyplot
import numpy as np
from matplotlib import pyplot as plt
import preprocess
import threading


running:bool = True
res = 20

def echo(args = ""):
    print(args)

def shutdown(args = ""):
    global running

    print("exiting...")
    running = False
    pass

cmd_list = {
    "echo":echo,
    "exit":shutdown,
    "y_thresh":preprocess.set_Y_thresh,
    "cr_thresh":preprocess.set_Cr_thresh,
    "cb_thresh":preprocess.set_Cb_thresh,
    "thresh":preprocess.set_threst_state,
    "values":preprocess.echo_tresh
}



def async_input():
    while running:

        cmd = input("/")
        cmd_split = cmd.split(" ",1)

        cmd_fun = cmd_list.get(cmd_split[0])

        if cmd_fun == None:
            continue
        
        if len(cmd_split) <= 1:
            cmd_fun()
            continue
        
        # print(*cmd_split[1:])

        try:
            cmd_fun(*cmd_split[1:])
        except Exception as e:
            print(e)

    pass

def main():
    

    input_thread = threading.Thread(target=async_input,args=())
    input_thread.start()
    # fp = easygui.fileopenbox()

    # frame = cv2.imread(fp)

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) #disable auto exposure
    cam.set(cv2.CAP_PROP_AUTOFOCUS, 0) #disable autofocus

    cam.set(cv2.CAP_PROP_FRAME_WIDTH,16*res)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT,9*res)
    # cam.set(cv2.CAP_PROP_EXPOSURE,1)
    # frame = preprocess.CreateHist(frame)

    while(running):
        ret, frame = cam.read()
        frame = cv2.flip(frame,1)

        pre, Y, CR, CB = preprocess.Isolate(frame)
        
        pre_stich = preprocess.mask_stitch(pre)



        # pre = cv2.multiply(CB,CR)
        # pre = cv2.bitwise_and(CR,CB)
        # pre = cv2.GaussianBlur(pre,(3,3),12)
        post_Y = cv2.multiply(pre,Y,scale=0.01)
        post_Ys = cv2.multiply(pre_stich,Y,scale=0.01)
        # post = cv2.merge([post_Y,post_Y, post_Y
        ret, post = cv2.threshold(post_Y,1,255,cv2.THRESH_BINARY)
        ret, posts = cv2.threshold(post_Ys,1,255,cv2.THRESH_BINARY)
        # print(type(post))

        # post = cv2.merge([post,post, post])
        
        # post = cv2.multiply(frame, post, scale= 1/255)
        # post = cv2.cvtColor(post, cv2.COLOR_YCR_CB2BGR)

        cv2.imshow('dist', posts)
        cv2.imshow('Camera', post)
        cv2.imshow('Y', Y)
        cv2.imshow('CR', CR)
        cv2.imshow('CB', CB)
        
        

        # plt.show(block = False) 
        key = cv2.waitKey(50)
        # if key == 27:
        #     break
        # break

    input_thread.join()

if __name__ == "__main__":
    main()