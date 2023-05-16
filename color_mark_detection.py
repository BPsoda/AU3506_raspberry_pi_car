import cv2
import numpy as np
import time

THRESH = {'blue':{'lower':(100, 70, 46), 'upper':(124, 255, 255)}}
Thresh_red = []



def blue_zone(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_zone = cv2.inRange(img_hsv, THRESH['blue']['lower'], THRESH['blue']['upper'])
    return np.sum(img_zone)/255

def red_zone(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_zone0 = cv2.inRange(img_hsv, (0,70,70), (10,255,255)) 
    img_zone1 = cv2.inRange(img_hsv, (156, 70, 70), (180, 255, 255)) 
    img_zone = np.logical_or(img_zone0, img_zone1).astype(np.uint8) * 255
    return np.sum(img_zone)/255

def detect_block_color(img):
    roi = [(0.33,0.65),(0.30,0.70)]
    shape = img.shape
    img_roi = img[round(shape[0]*roi[0][0]):round(shape[0]*roi[0][1]), 
                                        round(shape[1]*roi[1][0]):round(shape[1]*roi[1][1])]
    #cv2.imshow(' ', img_roi)
    #cv2.waitKey()
    flag = (blue_zone(img_roi)>45)
    if flag:
        print('block')
        cv2.imwrite('img_block/color_{}.png'.format(int(time.time())%100000), img)
        cv2.imwrite('img_block/color_roi_{}.png'.format(int(time.time())%100000), img_roi)
    return flag
    
if __name__ == '__main__':
    while 1:
        cap1 = cv2.VideoCapture(0)
        _, img = cap1.read()
        detect_block_color(img)
        cap1.release()
        
   #detect_color_zone(img)

