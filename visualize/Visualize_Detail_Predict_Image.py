from PIL import Image,ImageFont,ImageDraw
import os
import numpy as np

def Visualize_Detail_Predict_Image(imarray, save_path, height, width, coord_list,Label_List,Overall_Segment_Array):
    """
    :param imarray: image array
    :param save_path: save path
    :param height:
    :param width:
    :param coord_list: coordinate list
    :param Label_List: label list
    :param Overall_Segment_Array: segmentation marker
    :return:
    none
    visualize the detailed predictions.
    """
    overall_width = imarray.shape[0]
    overall_height = imarray.shape[1]
    tmp_array = np.zeros([overall_width, overall_height, 3])
    for j in range(overall_width):
        for k in range(overall_height):
            if Overall_Segment_Array[j,k]<=1:#1 is background
                continue
            tmp_array[j,k]=imarray[j,k]
    img = Image.fromarray(tmp_array.astype(np.uint8))
    tmp_img_path = os.path.join(save_path, "Detail_Segment.png")
    img.save(tmp_img_path)
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 65)
    draw = ImageDraw.Draw(img)
    for k in range(len(Label_List)):
        tmp_coord = coord_list[k]
        draw.text((tmp_coord[0]-height/2, tmp_coord[1]-width*2/3), str(Label_List[k]), fill=(255, 255, 255),
                  font=fnt,stroke_width=3,troke_fill=(255,0,0))
    tmp_img_path = os.path.join(save_path, "Detailed_Overall_Predict.png")
    img.save(tmp_img_path)

    tmp_img_path = os.path.join(save_path, "Detailed_Segment_Predict.png")
    #img = Image.fromarray(tmp_array.astype(np.uint8))
    #img[Overall_Segment_Array == -1] = [255, 0, 0]
    tmp_array = np.zeros([overall_width, overall_height, 3])
    for j in range(overall_width):
        for k in range(overall_height):
            if Overall_Segment_Array[j, k] ==- 1:
                tmp_array[j, k]=[255,0,0]
            else:
                tmp_array[j, k] = imarray[j, k]
    img = Image.fromarray(tmp_array.astype(np.uint8))
    draw = ImageDraw.Draw(img)
    for k in range(len(Label_List)):
        tmp_coord = coord_list[k]
        draw.text((tmp_coord[0] - height / 2, tmp_coord[1] - width * 2 / 3), str(Label_List[k]), fill=(255, 0, 0),
                  font=fnt, stroke_width=3, troke_fill=(255, 0, 0))
    img.save(tmp_img_path)

    tmp_img_path = os.path.join(save_path, "Detailed_Segment_Predict_indicateremove.png")
    # img = Image.fromarray(tmp_array.astype(np.uint8))
    # img[Overall_Segment_Array == -1] = [255, 0, 0]
    tmp_array = np.zeros([overall_width, overall_height, 3])
    for j in range(overall_width):
        for k in range(overall_height):
            if Overall_Segment_Array[j, k] == - 1:
                tmp_array[j, k] = [255, 0, 0]
            else:
                tmp_array[j, k] = imarray[j, k]
    img = Image.fromarray(tmp_array.astype(np.uint8))
    draw = ImageDraw.Draw(img)
    for k in range(len(Label_List)):
        tmp_coord = coord_list[k]
        draw.text((tmp_coord[0] - height / 2, tmp_coord[1] - width * 2 / 3), str(Label_List[k]), fill=(0,0,255),
                  font=fnt, stroke_width=3, troke_fill=(0, 0,255))
    img.save(tmp_img_path)
    #plot blue and red cubes
    tmp_img_path = os.path.join(save_path, "Detailed_Segment_Predict_Final.png")

    pos_coord = []
    neg_coord = []
    for k,tmp_coord in enumerate(coord_list):
        if Label_List[k]==1:
            pos_coord.append(tmp_coord)
        else:
            neg_coord.append(tmp_coord)
    tmp_array = Segment_Out_Coord(tmp_array, pos_coord, height, width, 0)
    tmp_array = Segment_Out_Coord(tmp_array, neg_coord, height, width, 1)
    img = Image.fromarray(tmp_array.astype(np.uint8))
    img.save(tmp_img_path)

def Segment_Out_Coord(imarray,pos_coord_list,height, width, color_type):
    if color_type==0:
        color_array=np.zeros(3)
        color_array[0]=255
    else:
        color_array = np.zeros(3)
        color_array[2] = 255
    pos_coord_list = np.array(pos_coord_list)
    overall_width = imarray.shape[0]
    overall_height = imarray.shape[1]
    for tmp_coord in pos_coord_list:
        tmp_x=tmp_coord[1]
        tmp_y=tmp_coord[0]#must switch to make sure matched with the correct postion in array
        ##in this label x is y, y is x
        # print(tmp_x,tmp_y)
        tmp_left = tmp_x - int(width / 2)
        tmp_bottom = tmp_y - int(height / 2)
        right_end = tmp_left + width if tmp_left + width < overall_width else overall_width
        upper_end = tmp_bottom + height if tmp_bottom + height < overall_height else overall_height
        left_start = 0 if tmp_left < 0 else tmp_left
        bottom_start = 0 if tmp_bottom < 0 else tmp_bottom
        imarray[left_start:right_end, bottom_start:upper_end, :]=\
            imarray[left_start:right_end, bottom_start:upper_end, :]*0.5+ 0.5*color_array
    return imarray
