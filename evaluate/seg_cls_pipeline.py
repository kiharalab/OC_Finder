import torch
from torch import nn
from model.Resnet import resnet20
import os
from ops.os_operation import mkdir
from ops.resize_img import resize_img
from PIL import Image
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from model.Load_CPU_Model import Load_CPU_Model
import shutil
from evaluate.segment_image import segment_image
from evaluate.clf_predict import clf_predict

def init_log_path(input_img_path,params):
    """
    :param input_img_path:
    :param params:
    :return:
    save path for segmentation and classification
    image name includes param information
    """
    log_path = os.path.join(os.getcwd(), 'Predict_Result')
    mkdir(log_path)
    split_path = os.path.split(input_img_path)
    origin_img_name = split_path[1][:-4]
    log_path = os.path.join(log_path, split_path[1])
    mkdir(log_path)
    log_path = os.path.join(log_path, "Filter_" + str(params['filter_size']))
    mkdir(log_path)
    origin_img_name += "Filter_" + str(params['filter_size'])
    log_path = os.path.join(log_path, "threshold_" + str(params['threshold']))
    mkdir(log_path)
    origin_img_name += "threshold_" + str(params['threshold'])
    log_path = os.path.join(log_path, "Removepixel_" + str(params['remove_pixel']))
    mkdir(log_path)
    origin_img_name += "Removepixel_" + str(params['remove_pixel'])
    return log_path, origin_img_name

def config_model(params,model_path):
    """
    :param params:
    :param model_path: trained model path
    :return:
    trained classification model
    """
    model = resnet20(num_class=params['class'])
    if params['choose'] != "-1":
        model = model.cuda()
        model = nn.DataParallel(model, device_ids=None)
    model_state_dict = torch.load(model_path, map_location='cpu')
    if 'ema_state_dict' in model_state_dict.keys():
        print("Load EMA model")
        if params['choose'] != "-1":
            msg = model.load_state_dict(model_state_dict['ema_state_dict'])
            print("loading model message: ", msg)
        else:
            model = Load_CPU_Model(model_state_dict['ema_state_dict'], model)
    else:
        print("Load common model")
        if params['choose'] != "-1":
            msg = model.load_state_dict(model_state_dict['state_dict'])
            print("loading model message: ", msg)
        else:
            model = Load_CPU_Model(model_state_dict['state_dict'], model)
    return model
def seg_cls_pipeline(params, input_img_path,  model_path):
    """
    :param params: configs
    :param input_img_path: input microscopy image
    :param model_path: trained classification model path
    :return:
    """
    log_path, origin_img_name = init_log_path(input_img_path,params)

    #load trained model
    model = config_model(params,model_path)

    save_path = log_path
    if params['resize']:
        print("We are doing resizing here")
        input_img_path_resize = os.path.join(save_path, 'resize_img.png')
        input_img_path = resize_img(input_img_path,params['resize_width'],
                                    params['resize_height'],input_img_path_resize)
    #segment image into differet areas
    Markers = segment_image(input_img_path, save_path, params)

    imarray = cv.imread(input_img_path)
    print("Markers shape", Markers.shape)  # same as image shape
    print("imarray type", type(imarray))
    #make predictions based on candidate segmented cell images
    clf_predict(model, Markers, imarray, save_path, params,origin_img_name)



