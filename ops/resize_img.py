import cv2 as cv
import os

def resize_img(input_img_path,width, height,input_img_path_resize):
    """
    :param input_img_path:
    :param width: resized width
    :param height: resized height
    :param input_img_path_resize: resized image path
    :return:
    resized image path
    """
    img = cv.imread(input_img_path)
    img2 = cv.resize(img, (width, height))
    cv.imwrite(input_img_path_resize, img2)
    return input_img_path_resize