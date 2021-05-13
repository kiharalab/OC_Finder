import shutil
import cv2 as cv
import os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

def segment_image(input_img_path, save_path, params):
    """
    :param input_img_path: input image path
    :param save_path: save segmented intermediate results
    :param params: configs
    :return:
    marker information indicates whether it's background(1), boundary(-1),
    removal segmented regions (-3) or waitiing detection region(>1).
    """
    # https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html
    original_path = os.path.join(save_path, 'Original.png')
    # os.system("cp "+input_img_path+" "+original_path)
    shutil.copy(input_img_path, original_path)
    img = cv.imread(input_img_path)
    if img is None:
        print("READING IMAGE FAILED!!")
        exit()
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #different binarization  methods
    if params['type'] == 0:
        ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    else:
        ret, thresh = cv.threshold(gray, params['threshold'], 255, cv.THRESH_BINARY_INV)
    # noise removal
    filter_size = params['filter_size']
    kernel = np.ones((filter_size, filter_size), np.uint8)
    # detailed instructions in https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    sure_bg = cv.dilate(opening, kernel, iterations=3)
    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 3)
    ret, sure_fg = cv.threshold(dist_transform, 3, 255, 0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)
    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0
    img1 = img.copy()
    markers = cv.watershed(img1, markers)
    # check the markers id
    max_id = np.max(markers)
    if params['remove_pixel'] != 0:
        remove_threshold = params['remove_pixel']

        for k in range(2, max_id + 1):
            remove_index = np.argwhere(markers == k)
            area_size = len(remove_index)
            if area_size < remove_threshold:
                markers[remove_index[:, 0], remove_index[:, 1]] = -3  # marked as not visiable

    img1[markers == -1] = [255, 0, 0]
    # save the image with watershed
    tmp_image = Image.fromarray(img1)
    extracted_path = os.path.join(save_path, "Filtered_watershed.png")
    tmp_image.save(extracted_path)
    if params['remove_pixel'] != 0:
        img1 = img.copy()
        remove_threshold = params['remove_pixel']
        markers2 = np.array(markers)
        for k in range(2, max_id + 1):
            remove_index = np.argwhere(markers2 == k)
            area_size = len(remove_index)
            if area_size < remove_threshold:
                markers2[remove_index[:, 0], remove_index[:, 1]] = -3  # marked as not visiable
            else:
                markers2[remove_index[:, 0], remove_index[:, 1]] = -1  # marked the regions inside boundary waiting to be classified.
        img1[markers2 == -3] = [0, 255, 0]
        img1[markers2 == -1] = [255, 0, 0]
        tmp_image = Image.fromarray(img1)
        extracted_path = os.path.join(save_path, "Filtered_removal.png")
        tmp_image.save(extracted_path)

    # colored markers
    markers_plot = np.array(markers, dtype=np.uint8)
    heat_map = cv.applyColorMap(markers_plot, cv.COLORMAP_JET)
    plt.imshow(heat_map, alpha=0.5)
    markers_path = os.path.join(save_path, "Markers_visualization.png")
    plt.savefig(markers_path)
    # show the extracted plots, block other parts
    remained_image = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if (markers[i, j] > 1):
                remained_image[i, j, :] = img[i, j, :]
    remained_image = np.array(remained_image, dtype=np.uint8)
    imgshow = Image.fromarray(remained_image)
    extracted_path = os.path.join(save_path, 'Extracted_area.png')
    imgshow.save(extracted_path)
    return markers