import numpy as np
import cv2

COLOR_THRESH = {'black': {'lower': (0,0,0), 'upper': (360, 255, 50)}}

def line_detection(view):
    '''detect the bias between lane and center of the image.
    Please make sure no crossing in the image.'''
    H, W, C = view.shape
    roi = [3/5, 1/5, 1/3, 1/3]  # region of interest, described in fraction [top, bottom, left, right]
    crop_img = view[int(roi[0]*H):int((1-roi[1])*H), int(roi[2]*W):int((1-roi[3])*W)]
    # cv2.imshow('roi', crop_img)
    # cv2.waitKey(0)
    height, width, _ = crop_img.shape
    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, COLOR_THRESH['black']['lower'], COLOR_THRESH['black']['upper'])
    # calculate the center of line
    m = cv2.moments(mask,False)
    try:
        cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
    except ZeroDivisionError:
        cx, cy = width/2, height/2
    error_x = cx - width / 2
    return error_x

if __name__ == '__main__':
    view = cv2.imread('../example/turn_left.jpg')
    print(line_detection(view))