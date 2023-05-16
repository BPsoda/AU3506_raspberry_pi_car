import cv2 
import time
COLOR_THRESH = {'black': {'lower': (0,0,0), 'upper': (360, 255, 100)}}


def is_block(view,thresh=350):
    H, W, C = view.shape

    roi = [1/3, 1/3, 1/10, 1/10]  # region of interest, described in fraction [top, bottom, left, right]
    crop_img = view[int(roi[0]*H):int((1-roi[1])*H), int(roi[2]*W):int((1-roi[3])*W)]
    crop_img = cv2.resize(crop_img, (100,100))
    # cv2.imshow('roi', crop_img)
    # cv2.waitKey(0)
    height, width, _ = crop_img.shape
    hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, COLOR_THRESH['black']['lower'], COLOR_THRESH['black']['upper'])
    # 创建结构元素
    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    #kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 50))
    
    # 进行闭操作
    closed_img = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel1)
    #closed_img = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel2)
    white_pixels = cv2.countNonZero(closed_img)
    ratio=white_pixels
    print(ratio)
    if (ratio>thresh):
        return False
    else:
        print('block detected!')
        ttt = int(time.time())%10000
        cv2.imwrite(f'img_block/{ttt}_block.png', view)
        cv2.imwrite(f'img_block/{ttt}_block_cut.png', crop_img)
        cv2.imwrite(f'img_block/{ttt}_block_cut_close.png', closed_img)
        return True
