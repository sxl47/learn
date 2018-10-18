#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_ocr.py
@time: 2018/5/8 10:43
@desc:

"""
import traceback

import cv2
import numpy as np

name_i = 0


def test1(img_name):
    import pytesseract as pytesseract
    from PIL import Image, ImageEnhance
    im = Image.open(img_name)
    enhancer = ImageEnhance.Color(im)
    enhancer = enhancer.enhance(0)
    enhancer = ImageEnhance.Brightness(enhancer)
    enhancer = enhancer.enhance(2)
    enhancer = ImageEnhance.Contrast(enhancer)
    enhancer = enhancer.enhance(8)
    enhancer = ImageEnhance.Sharpness(enhancer)
    im = enhancer.enhance(20)
    im.show()

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    ss = pytesseract.image_to_string(im)
    print(ss)


def split_img(path_name):
    """
    返回最小的矩形
    :param img: 图形
    :param is_up: 是否正上  True为正上的矩形，即不倾斜的，为False可能是倾斜的矩形
    :return:
    """
    img = cv2.imread(path_name)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_gray = cv2.Canny(img_gray, 100, 300, 10)
    # cv2.imshow("1", img_gray)
    # cv2.waitKey(0)

    (cnts, _) = cv2.findContours(img_gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

    color = (0, 255, 0)
    line_width = 2

    for c in cnts:
        rect = cv2.minAreaRect(c)
        rect = np.int0(cv2.cv.BoxPoints(rect))
        xs = [i[0] for i in rect]
        ys = [i[1] for i in rect]
        x1 = min(xs)
        x2 = max(xs)
        y1 = min(ys)
        y2 = max(ys)

        # cv2.rectangle(img, (x1, y1), (x2, y2), color, line_width)

        imt_tmp = img[y1:y2, x1:x2]
        # imt_tmp = img_gray[y1:y2, x1:x2]
        if len(imt_tmp) > 0:
            # cv2.imshow("binary", imt_tmp)
            # cv2.waitKey(0)
            global name_i
            name_i += 1
            cv2.imwrite("./tmp/{0}.jpg".format(name_i), imt_tmp)

    # cv2.imshow("binary", img)
    # cv2.waitKey(0)


def dilated_img(path_name):
    # 定义了一个5×5的十字形结构元素,
    # 用结构元素与其覆盖的二值图像做“与”操作
    # 如果都为1，结果图像的该像素为1。否则为0
    # 腐蚀处理的结果是使原来的二值图像减小一圈。
    # 00100
    # 00100
    # 11111
    # 00100
    # 00100
    kernel = np.uint8(np.zeros((5, 5)))
    for x in range(5):
        kernel[x, 2] = 1
        kernel[2, x] = 1
        # 读入图片
    img = cv2.imread(path_name, 0)
    # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    # 腐蚀图像
    # eroded = cv2.erode(img, kernel)
    # 膨胀图像
    dilated = cv2.dilate(img, kernel)

    path = "./dilated.jpg"
    # cv2.imwrite("./eroded.jpg", eroded)
    cv2.imwrite(path, dilated)

    return path


def split_imgs():
    import os
    file_dir = 'F:/sxl/sofa/src/py_proj/learn/tel_pic/'
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            # path_name = 'F:/sxl/sofa/src/py_proj/learn/tel_pic/135100759.png'
            path_name = root + file
            try:
                path = dilated_img(path_name)
                split_img(path)
            except Exception as e:
                traceback.print_exc(e)


def clip_img():
    import os
    file_dir = 'F:/sxl/sofa/src/py_proj/learn/tmp2/'
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            path_name = root + file
            try:
                img = cv2.imread(path_name)
                a = cv2.copyMakeBorder(img, 50, 50, 50, 50, cv2.BORDER_REFLECT)
            except Exception as e:
                traceback.print_exc(e)


def start():
    split_imgs()
    # test1('1.jpg')


if __name__ == '__main__':
    start()
