import numpy
import cv2
import time

from pid_controller import PID_Controller
from driver import driver
from line_detection import line_detection
from cross_detect import cross_detection
from sign_detect import sign_detection

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
        if cross_detection():
            cross_count += 1
            if cross_count in CROSS_FLAGS:
                # start turning right
                for i in range(10): 
                    driver.set_speed(RIGHT_INPLACE)
                continue
        # sign detection
        sign = sign_detection()
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

