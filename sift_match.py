#!/usr/bin/python
#coding=utf-8
import cv2
import time
from baseImage import Image
from image_registration.matching import SIFT

def SIFT_Detection(inputArray):
    match=SIFT(threshold=0.9, rgb=True, nfeatures=50000)
    im_source = Image.clone(inputArray)
    im_search_left= Image('test_left_module.png')
    im_search_right= Image('test_right_module.png')
    im_search_goal= Image('test_goal_module.png')
    im_search_left_array= Image('test_left_array_module.png')
    im_search_right_array=Image('test_right_array_module.png')
    search_modules=[im_search_left,im_search_right,im_search_goal,im_search_left_array,im_search_right_array]
    search_names=['左','右','靶子','左箭头','右箭头']
    start = time.time()
    result_with_name=[]
    for module,name in zip(search_modules,search_names):
        result = match.find_all_results(im_source, module)
        if (len(result)>0):
            result_with_name.append([name,result[0]])
    img = im_source.clone()
    if (len(result_with_name)==0):
        return "没有对应的匹配",img
    sorted_result = sorted(result_with_name, key=lambda x: x[1]['confidence'])
    info=f"发现了{sorted_result[0][0]}标识符,匹配相似度:{sorted_result[0][1]['confidence']}"
    print("use:",time.time() - start,"s")
    img.rectangle(rect=sorted_result[0][1]['rect'], color=(0, 0, 255), thickness=3)
    return info,img

if __name__=="__main__":
    # match = SIFT()
    im_source = Image('test_goal.png')
    im_search = Image('test_left_module.png')

    # start = time.time()
    # result = match.find_all_results(im_source, im_search)
    # print(time.time() - start)
    # print(result)
    # img = im_source.clone()
    # for _ in result:
    #     img.rectangle(rect=_['rect'], color=(0, 0, 255), thickness=3)
    # img.imshow('ret')
    # cv2.waitKey(0)
    info,img=SIFT_Detection(im_source)
    print(info)
    # img.imshow('img',img)
    # cv2.waitKey(0)
    