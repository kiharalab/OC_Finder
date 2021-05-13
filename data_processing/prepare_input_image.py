import numpy as np
import os
from PIL import Image
from ops.os_operation import mkdir


def prepare_input_image(imarray,save_path,count_image,height,width,pos_coord_list,label):
    overall_width=imarray.shape[0]
    overall_height=imarray.shape[1]
    #print(overall_width,overall_height)
    pos_coord_list=np.array(pos_coord_list)
    max_x=np.max(pos_coord_list[:,0])
    max_y = np.max(pos_coord_list[:, 1])
    print("Checking agreement of shape:%d/%d,%d/%d"%(max_y,overall_width,max_x,overall_height))
    for tmp_coord in pos_coord_list:
        tmp_x=tmp_coord[1]
        tmp_y=tmp_coord[0]#must switch to make sure matched with the correct postion in array
        ##in this label x is y, y is x

        #print(tmp_x,tmp_y)
        tmp_left=tmp_x-int(width/2)
        tmp_bottom=tmp_y-int(height/2)
        #print(tmp_left,tmp_bottom)
        tmp_array=np.zeros([width,height,3])
        right_end=tmp_left+width if tmp_left+width<overall_width else overall_width
        upper_end=tmp_bottom+height if tmp_bottom+height<overall_height else overall_height
        #print(right_end,upper_end)
        left_start=0 if tmp_left<0 else tmp_left
        bottom_start=0 if tmp_bottom<0 else tmp_bottom
        tmp_width=int(right_end-left_start)
        tmp_height=int(upper_end-bottom_start)
        #print(tmp_width,tmp_height)
        tmp_left_start=int((width-tmp_width)/2)
        tmp_bottom_start=int((height-tmp_height)/2)
        tmp_array[tmp_left_start:tmp_left_start+tmp_width,tmp_bottom_start:tmp_height+tmp_bottom_start,:]=\
            imarray[left_start:right_end,bottom_start:upper_end,:]#set to center for new image
        #tmp_array=imarray[tmp_left:tmp_left+width,tmp_bottom:tmp_bottom+height,:]
        tmp_train_path=os.path.join(save_path,'trainset'+str(count_image)+'.npy')
        tmp_aim_path=os.path.join(save_path,'aimset'+str(count_image)+'.npy')
        np.save(tmp_train_path,tmp_array)
        np.save(tmp_aim_path, np.array(label))
        img=Image.fromarray(tmp_array.astype(np.uint8))
        tmp_img_path=os.path.join(save_path,str(label)+"_"+str(count_image)+'.png')
        img.save(tmp_img_path)
        count_image+=1
    return count_image