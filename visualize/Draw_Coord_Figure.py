from PIL import Image,ImageFont,ImageDraw,ImageFont
import numpy as np

def Draw_Coord_Figure(tmp_coord_figure_path,coord_list,imarray,height,width):
    """
    :param tmp_coord_figure_path: save path
    :param coord_list:
    :param imarray:
    :param height:
    :param width:
    :return:
    indicate the identified locations in the microscopy image
    """
    #print(imarray)
    #print(imarray.shape)
    modify_imarray=np.array(imarray,dtype=np.uint8)
    img=Image.fromarray(modify_imarray)
    #fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 65)
    fnt = ImageFont.load_default()
    #img = Image.fromarray(imarray.astype(np.uint8))
    draw = ImageDraw.Draw(img)
    for k in range(len(coord_list)):
        tmp_coord = coord_list[k]
        draw.text((tmp_coord[0]-height/2, tmp_coord[1]-width*2/3), "C", font=fnt,fill=(255,0, 0),stroke_width=3,
          stroke_fill=(255,0,0))
    img.save(tmp_coord_figure_path)