import numpy as np
import cv2
from driver import driver

car = driver()


def one_same():
    x = 40
    y = 40
    return x, y


def diff_left():
    x = 80
    y = 40
    return x, y


def diff_right():
    x = 40
    y = 80
    return x, y

cap1 = cv2.VideoCapture(0)

while True:
    _, frame1 = cap1.read()
    cv2.imshow("image1",frame1)
    key = cv2.waitKey(3)
    if key == ord('w'):
        car.set_speed(one_same()[0], one_same()[1])
    elif key == ord('a'):
        car.set_speed(diff_left()[0], diff_left()[1])
    elif key == ord('d'):
        car.set_speed(diff_right()[0], diff_right()[1])
    elif key == ord('s'):
        car.set_speed(-one_same()[0], -one_same()[1])
    else:
        car.set_speed(0, 0)
