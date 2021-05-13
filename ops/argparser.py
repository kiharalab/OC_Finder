#
# Copyright (C) 2018 Xiao Wang
# Email:xiaowang20140001@gmail.com
#

import parser
import argparse

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-F',type=str, required=True,help='input microscopy image path')
    parser.add_argument('--mode',type=int,required=True,help='0: single image processing;\n 1: multiple image processing')
    parser.add_argument('--type',type=int,default=0,help='setting type: 0: common setting;\n 1: including large cells')
    parser.add_argument('--choose',type=str,default='0',help='gpu id choose for training, if you use -1 means you do not use gpu')
    parser.add_argument('--class', type=int, default='2', help='number of classes')
    parser.add_argument('--cardinality',default=32, type=int,help='ResNeXt cardinality')
    parser.add_argument('--batch_size', type=int, default=128, help='batch size for training')
    parser.add_argument('-M', type=str, default="best_model/ema_best.pth.tar", help='trained model path of OC_Finder')  # File path for our MAINMAST code
    parser.add_argument('--width',type=int,default=50,help="Width of classification image")
    parser.add_argument('--height',type=int,default=50,help="Height of classification image")
    parser.add_argument('--num_workers', type=int, default=4, help="number of workers for the dataloader")
    parser.add_argument('--resize',default=0,type=int,help="if we need resize the input microscopy image or not. default: 0(no resizing)")
    parser.add_argument('--resize_height',default=200,type=int,help="The resized image height used for the segmentation")
    parser.add_argument('--resize_width', default=200, type=int,help="The resized image width used for the segmentation")
    parser.add_argument('--filter_size',default=3,type=int,help="user can adjust their own filter size to have different segmentation results. default:3")
    parser.add_argument('--threshold',default=195,type=int,help="Threshold used to do image segmentation (Suggested 150-210 for big cell cases)")
    parser.add_argument('--remove_pixel',default=500,type=int,help="number of pixels to remove small segmented regions. default: 500")
    args = parser.parse_args()
    params = vars(args)
    return params