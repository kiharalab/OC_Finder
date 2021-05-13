import os
import numpy as np

def load_input_array(save_path,count_image):
    """
    :param save_path: input save path
    :param count_iamge: the input numpy array
    :return:
    concatenated input array
    """
    All_Predict_Img = []
    for k in range(count_image):
        tmp_trainset_path = os.path.join(save_path, 'trainset' + str(k) + '.npy')
        tmp_array = np.load(tmp_trainset_path)
        All_Predict_Img.append(tmp_array)
    All_Predict_Img = np.array(All_Predict_Img)
    return All_Predict_Img