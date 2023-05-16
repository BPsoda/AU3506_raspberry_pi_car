
import cv2
import numpy as np
import time
modules=['img/test_left_module.png','img/test_right_module.png','img/test_goal_module.png','img/test_left_array_module.png','img/test_right_array_module.png']
SEARCH_NAMES = ['左', '右', '靶子', '左箭头', '右箭头']
templates=[]
for sample in modules:
    template = cv2.imdecode(np.fromfile(sample, dtype=np.uint8), cv2.IMREAD_COLOR)
    template = cv2.resize(template, (100,100))
    templates.append(template)

def Perspective(img,corners):

    src=np.float32(corners)
    # print(src)
    dst = np.float32([[0, 0], [0, 100], [100, 100], [100, 0]])
    M = cv2.getPerspectiveTransform(src, dst)

    # 进行透视变换
    warped = cv2.warpPerspective(img, M, (100, 100))
    return warped
def mser_image_processing(image):
 
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    visual = image.copy()
    original = gray.copy()
 
    mser = cv2.MSER_create()
    regions,_=mser.detectRegions(gray)
    hulls = [cv2.convexHull(p.reshape(-1,1,2)) for p in regions]
    cv2.polylines(image,hulls,1,(0,255,0))
    # cv2.imshow("image",image)
    
    keep=[]
    for c in hulls:
        x,y,w,h = cv2.boundingRect(c)
        keep.append([x,y,x+w,y+h])
        #cv2.rectangle(visual,(x,y),(x+w,y+h),(255,255,0),1)
    keep = np.array(keep)
    boxes = nms(keep,0.5)
    scores = []
    count=0
    for box in boxes:
        if (0.9<(box[2]-box[0])/(box[3]-box[1])<1.1 and  (box[3]-box[1])>60):
            # cv2.rectangle(visual, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 1)
            corner=[[box[0],box[1]],[box[0],box[3]],[box[2],box[3]],[box[2],box[1]]]
            warp=Perspective(visual,corner)
            cv2.imwrite(f'fig_{count}.png',warp)
            count+=1
            #cv2.imshow('warp',warp)
            #cv2.waitKey(0)
            for template in templates[:2]:
                scores.append(cv2.matchTemplate(warp,template,cv2.TM_CCOEFF_NORMED)[0][0])
    index = np.argmax(np.array(scores))%5
    res=SEARCH_NAMES[index]
    print(res)
            # img_corp=visual[box[1]:box[3],box[0]:box[2]]
            
            # cv2.imshow("corp",img_corp)
            # cv2.waitKey(0)
    # cv2.imshow("hulls",visual)
    # cv2.waitKey(0)
    return visual,res
# NMS 方法（Non Maximum Suppression，非极大值抑制）
def nms(boxes, overlapThresh):
    if len(boxes) == 0:
        return []
 
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
 
    pick = []
 
    # 取四个坐标数组
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
 
    # 计算面积数组
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
 
    # 按得分排序（如没有置信度得分，可按坐标从小到大排序，如右下角坐标）
    idxs = np.argsort(y2)
 
    # 开始遍历，并删除重复的框
    while len(idxs) > 0:
        # 将最右下方的框放入pick数组
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
 
        # 找剩下的其余框中最大坐标和最小坐标
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
 
        # 计算重叠面积占对应框的比例，即 IoU
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / area[idxs[:last]]
 
        # 如果 IoU 大于指定阈值，则删除
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))
 
    return boxes[pick].astype("int")
 
 
if __name__ == '__main__':
    start = time.time()
    img = cv2.imread('img/color_40919.png', cv2.IMREAD_COLOR)
    mser_image_processing(img)
    print("use:",time.time() - start,"s")
    # cv2.waitKey(0)
