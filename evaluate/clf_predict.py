from torch.autograd import Variable
import torch.nn.functional as F
import torch
from torch import nn
from torch import optim
import numpy as np
import os
from PIL import Image,ImageFont,ImageDraw,ImageFont
import shutil
from visualize.Draw_Coord_Figure import Draw_Coord_Figure
from data_processing.prepare_input_image import prepare_input_image
from ops.os_operation import mkdir
from data_processing.load_input_array import load_input_array
from data_processing.Single_Dataset import SingleTestDataset
from evaluate.model_inference import model_inference
from data_processing.relabel_input_image import relabel_input_image
from visualize.Visualize_Predict_Image import Visualize_Predict_Image
from visualize.Visualize_Detail_Predict_Image import Visualize_Detail_Predict_Image
def Build_Coord_List(Overall_Segment_Array):
    """
    :param Overall_Segment_Array: segmentation indicator array
    :return:
    center coord list for predictions
    """
    Final_Coord=[]
    label_list=np.unique(Overall_Segment_Array)
    print("In total, we have %d segmented areas waiting to be predicted"%(len(label_list)-3))
    for tmp_label in label_list:
        if tmp_label<=1:
            continue
        Coord_List=np.argwhere(Overall_Segment_Array==tmp_label)
        X_list=[]
        Y_list=[]
        for tmp_coord in Coord_List:
            X_list.append(tmp_coord[0])
            Y_list.append(tmp_coord[1])
        X_list=np.array(X_list)
        Y_list=np.array(Y_list)
        if len(X_list)==0:
            continue
        X_mean=int(np.mean(X_list))
        Y_mean=int(np.mean(Y_list))
        Final_Coord.append([X_mean,Y_mean])
    return Final_Coord

def clf_predict(model, Overall_Segment_Array, imarray, save_path, params,origin_img_name):
    """
    :param model: trained model
    :param Markers: segmented info array
    :param imarray: image array
    :param save_path: save path
    :param params: configs
    :param origin_img_name: image name
    :return:
    """
    mean_value = (0.59187051, 0.53104666, 0.56797799)
    std_value = (0.19646512, 0.23195337, 0.20233912)
    height = params['height']
    width = params['width']
    #locating center coord for input images
    coord_list = Build_Coord_List(Overall_Segment_Array)  # this coord for imarray not for image
    # change x,y locations, now the coord is back to images
    new_coord_list = []
    for coord in coord_list:
        new_coord_list.append([coord[1], coord[0]])
    coord_list = new_coord_list
    coord_list = np.array(coord_list)  # coord now is based on image, instead of array
    tmp_coord_path = os.path.join(save_path, 'Coord_Info.txt')
    np.savetxt(tmp_coord_path, coord_list)
    print("DEBUG INFO: im array type", type(imarray))
    #visualize candidate image center
    tmp_coord_figure_path = os.path.join(save_path, "Coord_Info.png")
    Draw_Coord_Figure(tmp_coord_figure_path, coord_list, imarray, height, width)

    #extract the candidate image for feeding into network
    feature_save_path = os.path.join(save_path,"input")
    mkdir(feature_save_path)
    count_image1 = 0
    count_image1 = prepare_input_image(imarray,feature_save_path,count_image1,height,width,coord_list,0)
    if count_image1 == len(coord_list):
        print("Successfully segmented image and saved!!!")
    else:
        print("Segmented part can not work, please have a check")
        return
    All_Predict_Img = load_input_array(feature_save_path,count_image1)

    #feeding to dataloader

    valid_dataset = SingleTestDataset(All_Predict_Img, mean_value, std_value)
    test_dataloader = torch.utils.data.DataLoader(valid_dataset, batch_size=params['batch_size'],
                                                  shuffle=False, num_workers=int(params['num_workers']),
                                                drop_last=False, pin_memory=True)
    #making predicitons
    label_list = model_inference(model, test_dataloader, params, save_path, origin_img_name, coord_list)
    relabel_input_image(count_image1, feature_save_path,label_list)
    Visualize_Predict_Image(imarray, save_path, height, width, coord_list, label_list)
    Visualize_Detail_Predict_Image(imarray, save_path, height, width, coord_list,label_list, Overall_Segment_Array)




