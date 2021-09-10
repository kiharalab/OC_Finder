from PIL import Image,ImageFont,ImageDraw
import os
import numpy as np

def Visualize_Predict_Image(imarray, save_path, height, width, coord_list,Label_List):
    """
    :param imarray: image array
    :param save_path:
    :param height:
    :param width:
    :param coord_list: coordinate list
    :param Label_List: predicted label
    :return:
    """
    overall_width = imarray.shape[0]
    overall_height = imarray.shape[1]
    tmp_array = np.zeros([overall_width, overall_height, 3])
    coord_list = np.array(coord_list)
    max_x = np.max(coord_list[:, 0])#coord based on image
    max_y = np.max(coord_list[:, 1])
    print("1 Checking agreement of shape:%d/%d,%d/%d" % (max_y, overall_width, max_x, overall_height))
    for tmp_coord in coord_list:
        tmp_x=tmp_coord[1]
        tmp_y=tmp_coord[0]
        tmp_left=tmp_x-int(width/2)
        tmp_bottom=tmp_y-int(height/2)
        right_end = tmp_left + width if tmp_left + width < overall_width else overall_width
        upper_end = tmp_bottom + height if tmp_bottom + height < overall_height else overall_height
        # print(right_end,upper_end)
        left_start = 0 if tmp_left < 0 else tmp_left
        bottom_start = 0 if tmp_bottom < 0 else tmp_bottom
        tmp_width = int(right_end - left_start)
        tmp_height = int(upper_end - bottom_start)
        # print(tmp_width,tmp_height)
        tmp_left_start = int((width - tmp_width) / 2)
        tmp_bottom_start = int((height - tmp_height) / 2)
        tmp_array[left_start:right_end, bottom_start:upper_end, :] = \
            imarray[left_start:right_end, bottom_start:upper_end, :]
    img = Image.fromarray(tmp_array.astype(np.uint8))
    tmp_img_path = os.path.join(save_path, "Overall_Segment.png")
    img.save(tmp_img_path)
    img_origin=Image.fromarray(imarray.astype(np.uint8))
    tmp_img_path = os.path.join(save_path, "Original.png")
    img_origin.save(tmp_img_path)
    draw = ImageDraw.Draw(img)
    #fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf",65)
    fnt = ImageFont.load_default()
    for k in range(len(Label_List)):
        tmp_coord=coord_list[k]
        draw.text((tmp_coord[0]-width/2, tmp_coord[1]-height*2/3),str(Label_List[k]) ,font=fnt, fill=(255, 0, 0),stroke_width=3,
          stroke_fill=(255,0,0))
    tmp_img_path = os.path.join(save_path, "Overall_Predict.png")
    img.save(tmp_img_path)
