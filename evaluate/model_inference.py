
import numpy as np
from torch.autograd import Variable
import torch.nn.functional as F
import os


def model_inference(model,test_dataloader,params,save_path,added_name,coord_list):
    """
    inference of the model and save predictions
    :param model:
    :param test_dataloader: data loader
    :param params:
    :param save_path: prediction saving path
    :param added_name: output prediction file name
    :param coord_list: coordinate array
    :return:
    output labels
    """
    Label_List = []
    Prob_List = []
    model.eval()  # very important, fix batch normalization
    for i, inputs in enumerate(test_dataloader):
        if params['choose'] != "-1":
            inputs = inputs.cuda()
            inputs = Variable(inputs, volatile=True)
        outputs, p1 = model(inputs)
        outputs = F.softmax(outputs, dim=1)
        if params['choose'] != "-1":
            outputs = outputs.cpu().detach().numpy()
        else:
            outputs = outputs.detach().numpy()
        for k in range(len(outputs)):
            tmp_pred = outputs[k]
            tmp_label = int(np.argmax(tmp_pred))
            Label_List.append(tmp_label)
            Prob_List.append(tmp_pred[tmp_label])
    pred_txt = os.path.join(save_path, 'Predict_' + str(added_name) + '.txt')
    count_positive = 0
    with open(pred_txt, 'w') as file:
        file.write('Coord0\tCoord_1\tPredict_Label\tProbability\n')
        for k in range(len(coord_list)):
            coord_info = coord_list[k]
            pred_info = Label_List[k]
            if pred_info == 1:
                count_positive += 1
            prob_info = Prob_List[k]
            file.write(str(coord_info[0]) + "\t" + str(coord_info[1]) + "\t" +
                str(pred_info) + "\t" + str(prob_info) + "\n")
    #write count results
    pred_txt = os.path.join(save_path, 'Predict_' + str(added_name) + '_pcount.txt')
    with open(pred_txt, 'w') as file:
        file.write('Total Positive:%d\n' % count_positive)
    return Label_List