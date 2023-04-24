#!/usr/bin/python
#coding=utf-8
import cv2
import time
from baseImage import Image
from image_registration.matching import ORB
import concurrent.futures
from functools import lru_cache

# 定义全局变量
SEARCH_MODULES = [
    Image('img/test_left_module.png'),
    Image('img/test_right_module.png'),
    Image('img/test_goal_module.png'),
    Image('img/test_left_array_module.png'),
    Image('img/test_right_array_module.png')
]
SEARCH_NAMES = ['左', '右', '靶子', '左箭头', '右箭头']

# 定义ORB匹配器
MATCHER = ORB(threshold=0.9, rgb=True, nfeatures=50000)

@lru_cache(maxsize=None)
def search_module(im_source):
    # 多线程处理，同时搜索多个图像
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(MATCHER.find_all_results, im_source, module) for module in SEARCH_MODULES]

    result_with_name = []
    for future, name in zip(futures, SEARCH_NAMES):
        result = future.result()
        if len(result) > 0:
            if (result[0]['confidence']>0.9):
                result_with_name.append([name, result[0]])
                break
            # result_with_name.append([name, result[0]])

    return result_with_name

@lru_cache(maxsize=None)
def SIFT_Detection(inputArray):
    im_source = Image(inputArray)
    start = time.time()
    result_with_name = search_module(im_source)
    img = im_source.clone()
    if len(result_with_name) == 0:
        return "没有对应的匹配", img
    sorted_result = sorted(result_with_name, key=lambda x: x[1]['confidence'])
    info="发现了{}标识符,匹配相似度:{}".format(sorted_result[0][0], sorted_result[0][1]['confidence'])
    print("use:",time.time() - start,"s")
    img.rectangle(rect=sorted_result[0][1]['rect'], color=(0, 0, 255), thickness=3)

    print("use:", time.time() - start, "s")
    return info, img

if __name__ == "__main__":
    im_source = Image('img/test_goal.png')
    im_source2 = Image('img/test_array_left.png')
    for _ in range(3):
        info, img = SIFT_Detection(im_source2)
        print(info)
    for _ in range(2):
        info, img = SIFT_Detection(im_source)
        print(info)
    for _ in range(3):
        info, img = SIFT_Detection(im_source2)
        print(info)
    # img.imshow('img', img)
    # cv2.waitKey(0)
