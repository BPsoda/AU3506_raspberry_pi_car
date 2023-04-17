import cv2
import numpy as np
COLOR_THRESH_CROSS_DETECTION = {'black': {'lower': (0,0,0), 'upper': (360, 255, 80)}}
THRESHOLD_CROSSING_DETECTION = 5000

def detect_crossing(img):
    roi = [(0.4,0.8),(0.2,0.8)]
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    img_black_zone = cv2.inRange(img_hsv, COLOR_THRESH_CROSS_DETECTION['black']['lower'], COLOR_THRESH_CROSS_DETECTION['black']['upper'])
    shape = img_black_zone.shape
    img_roi = img_black_zone[round(shape[0]*roi[0][0]):round(shape[0]*roi[0][1]), 
                                        round(shape[1]*roi[1][0]):round(shape[1]*roi[1][1])]
    
    structure = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (100, 3))
    img_closed = cv2.morphologyEx(img_roi, cv2.MORPH_CLOSE, structure)
    img_opened = cv2.morphologyEx(img_closed, cv2.MORPH_OPEN, structure)
    res = np.sum(img_opened // 255)
    print(res)

    cv2.imshow(" ", img_opened)
    cv2.waitKey()
    return res > THRESHOLD_CROSSING_DETECTION


if __name__=="__main__":
    img = cv2.imread('imgs/Crossing.jpg')
    detect_crossing(img)