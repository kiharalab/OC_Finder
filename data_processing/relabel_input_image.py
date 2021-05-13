import os
import shutil


def relabel_input_image(count_image1,save_path,Label_List):
    """
    :param count_image1:
    :param save_path:
    :param Label_List: predicted label
    :return:
    relabel the input image name based on our predictions
    """
    for k in range(count_image1):
        tmp_img_path = os.path.join(save_path, str(0) + "_" + str(k) + '.png')
        now_img_path = os.path.join(save_path, str(Label_List[k]) + "_" + str(k) + '.png')
        if now_img_path == tmp_img_path:
            continue
        if os.path.exists(now_img_path) and now_img_path != tmp_img_path:
            os.remove(now_img_path)
        # os.system("mv "+str(tmp_img_path)+" "+now_img_path)
        shutil.move(tmp_img_path, now_img_path)