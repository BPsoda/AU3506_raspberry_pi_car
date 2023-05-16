#!/usr/bin/python
#coding=utf-8
import numpy
import cv2
import time

from pid_controller import PID_Controller
from driver import driver
from line_detection import line_detection
from cross_detect import detect_crossing
from sign_detect import sign_detection
from mser_detect import *
from is_block import *
from color_mark_detection import *
CROSS_FLAGS = [2, 4]

# move
STRAIGHT = (4,4)
RIGHT_INPLACE = (-20, 20)
LEFT_INPLACE = (20, -20)

if __name__ == '__main__':
    # initialize video capture
    cap1 = cv2.VideoCapture(0)
    time1 = time.time()
    frame_cnt = 0
    fps = cap1.get(cv2.CAP_PROP_FPS)

    # objects
    controller = PID_Controller(0.02,0,0,-3,3)
    car = driver()
    cross_count = 0
    while True:
        _, frame1 = cap1.read()
        frame_cnt += 1
        ## if delay exceeds one frame, read until we get the newest frame
        #time2 = time.time()
        #delays = (time2-time1)*fps - frame_cnt
        #print("delays: {}".format(delays))
        #while delays > 0:
        #    _,frame1 = cap1.read()
        #    frame_cnt += 1
        #    time2 = time.time()
        #    delays = (time2-time1)*fps - frame_cnt
        if frame_cnt % 30 == 29:
            print("Rest camera")
            cap1.release()
            cap1 = cv2.VideoCapture(0)
            _, frame1 = cap1.read()
            
        # crossing detection
        if detect_crossing(img = frame1):
            cross_count += 1
            if 1 or cross_count in CROSS_FLAGS:
                # start turning right
                for i in range(40): 
                    car.set_speed(40, 40)
                    _, frame1 = cap1.read()
                for i in range(60): 
                    car.set_speed(RIGHT_INPLACE[0], RIGHT_INPLACE[1])
                    _, frame1 = cap1.read()
                continue
        # sign detection
        
        if (detect_block_color(frame1)):
        
            car.set_speed(0,0)
            cv2.imwrite('img_block/color_{}.png'.format(int(time.time())%100000), frame1)
            img,info=mser_image_processing(frame1)
            print(info)
            print("Rest camera")
            cap1.release()
            cap1 = cv2.VideoCapture(0)
            _, frame1 = cap1.read()
        
        
        # if sign == ...:
        #     ...
        #     continue
        # elif sign == ...:
        #     ...
        #     continue
        # lane keep
        error = line_detection(frame1)
        # print('err = ',error)
        dv = controller.get_output(error)
        # print('dv = ', dv)
        car.set_speed((4-dv)*10, (4+dv)*10)

