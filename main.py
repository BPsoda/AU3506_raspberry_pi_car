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
from sift_match import SIFT_Detection
CROSS_FLAGS = [2, 4]

# move
STRAIGHT = (4,4)
RIGHT_INPLACE = (-4, 4)
LEFT_INPLACE = (4,-4)

if __name__ == '__main__':
    # initialize video capture
    cap1 = cv2.VideoCapture(0)

    # objects
    controller = PID_Controller(1,0,0,-1,1)
    car = driver()
    cross_count = 0
    while True:
        _, frame1 = cap1.read()
        # crossing detection
        if detect_crossing():
            cross_count += 1
            if cross_count in CROSS_FLAGS:
                # start turning right
                for i in range(10): driver.set_speed(RIGHT_INPLACE)
                continue
        # sign detection
        info,img=SIFT_Detection(frame1)
        print(info)
        # if sign == ...:
        #     ...
        #     continue
        # elif sign == ...:
        #     ...
        #     continue
        # lane keep
        error = line_detection(frame1)
        dv = controller.get_output(error)
        car.set_speed([4, 4+dv])

