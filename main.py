
import os
from ops.argparser import argparser

if __name__ == "__main__":
    params = argparser()
    print("commanding params: ",params)
    if params['mode']==0:
        input_img_path = params['F']
        model_path = params['M']
        if params['choose']!="-1":
            choose = params['choose']
            os.environ["CUDA_VISIBLE_DEVICES"] = choose
        else:
            os.environ["CUDA_VISIBLE_DEVICES"] ="99999"#indicates no gpu
        from evaluate.seg_cls_pipeline import seg_cls_pipeline

        seg_cls_pipeline(params, input_img_path, model_path)

    elif params['mode']==1:
        input_img_dir = params['F']
        model_path = params['M']
        if params['choose'] != "-1":
            choose = params['choose']
            os.environ["CUDA_VISIBLE_DEVICES"] = choose
        else:
            os.environ["CUDA_VISIBLE_DEVICES"] = "99999"
            # if you want, you can also give the segmentation different filter size
        from evaluate.seg_cls_pipeline import seg_cls_pipeline

        listfiles = os.listdir(input_img_dir)
        for item in listfiles:
            tmp_file = os.path.join(input_img_dir, item)
            seg_cls_pipeline(params, tmp_file, model_path)