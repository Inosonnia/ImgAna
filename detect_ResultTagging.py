#!/bin/env python
#coding:utf-8
import glob
import sys
import os
import shutil
import random

from PIL import Image
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg

import xml.etree.ElementTree as ET
from pylab import *
def get_ext_files(targdir, ext):
    return filter(lambda x: x.endswith(ext), os.listdir(targdir))

def parse_annotation(annotation):
    tree = ET.ElementTree(file=annotation)
    root = tree.getroot()

    names = []
    xx0 = []
    yy0 = []
    xx1 = []
    yy1 = []
    for obj in root.iterfind('object'):
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        names.append(name)
        xx0.append(float(xmin))
        yy0.append(float(ymin))
        xx1.append(float(xmax))
        yy1.append(float(ymax))
    return names, xx0, yy0, xx1, yy1


def get_color_list(imgname):
    if imgname == '1':
        pltcolor = 'r'
    elif imgname == '5':
        pltcolor = 'g'
    elif imgname == '6':
        pltcolor = 'b'
    elif imgname == '7':
        pltcolor = 'c'
    elif imgname == '8':
        pltcolor = 'y'
    else:
        pltcolor = 'k'
    return pltcolor
    # print xx0, yy0, xx1, yy1   


def plot_rectangle(img, imgname, iname, xx0, yy0, xx1, yy1):
    plt.imshow(img)
    plt.title(iname)
    currentAxis = plt.gca()
    for i in range(len(xx0)):
        pltcolor = get_color_list(imgname[ i ])
        currentAxis.add_patch(Rectangle((xx0[ i ], yy0[ i ]), xx1[ i ] - xx0[ i ], yy1[ i ] - yy0[ i ], alpha=0.2, color = pltcolor))
    plt.show()
    # print xx0, yy0, xx1, yy1    

 
def dt_tagging(src_path):
    curname = src_path.split('VOCdevkit')[ 1 ]

    img_folder = os.path.join(src_path, 'VOC' + curname, "JPEGImages")
    result_folder = os.path.join(src_path, "results", 'VOC' + curname, "Main")

    ext = '.jpg'
    img_files = get_ext_files(img_folder, ext)

    ext = '.txt'
    res_files = get_ext_files(result_folder, ext)

    # print img_files
    # print res_files

    for imgname in img_files:
        org_img = Image.open(os.path.join(img_folder, imgname))

        for each_res_file in res_files:

            res_cls = each_res_file.split('trainval_')[ 1 ].split('.txt')[ 0 ]

            reader = open(os.path.join(result_folder, each_res_file), 'r')

            names = []
            xx0 = []
            yy0 = []
            xx1 = []
            yy1 = []
            conf = []

            while 1:
                line = reader.readline()

                if not line:
                    break

                strs = line.split(" ")
                # print cmp(strs[ 0 ], imgname.split(".jpg")[ 0 ]), strs[ 0 ], imgname.split(".jpg")[ 0 ]
                if not cmp(strs[ 0 ], imgname.split(".jpg")[ 0 ]):

                    names.append(res_cls)
                    conf.append(float(strs[ 1 ]))
                    xx0.append(float(strs[ 2 ]))
                    yy0.append(float(strs[ 3 ]))
                    xx1.append(float(strs[ 4 ]))
                    yy1.append(float(strs[ 5 ]))

            plot_rectangle(org_img, names, imgname, xx0, yy0, xx1, yy1)




def gt_tagging(src_path):
    curname = src_path.split('VOCdevkit')[ 1 ]

    img_folder = os.path.join(src_path, 'VOC' + curname, "JPEGImages")
    anno_folder = os.path.join(src_path, 'VOC' + curname, "Annotations")

    ext = '.jpg'
    img_files = get_ext_files(img_folder, ext)

    ext = '.xml'
    res_files = get_ext_files(anno_folder, ext)

    # print img_files
    # print res_files

    for imgname in img_files:
        org_img = Image.open(os.path.join(img_folder, imgname))
        org_anno = os.path.join(anno_folder, imgname.split(".jpg")[ 0 ] + ".xml")

        names, xmin, ymin, xmax, ymax = parse_annotation(org_anno)
        plot_rectangle(org_img, names, imgname, xmin, ymin, xmax, ymax)



def plot_compare_result_with_gt(src_path):
    curname = src_path.split('VOCdevkit')[ 1 ]

    img_folder = os.path.join(src_path, 'VOC' + curname, "JPEGImages")
    anno_folder = os.path.join(src_path, 'VOC' + curname, "Annotations")
    result_folder = os.path.join(src_path, "results", 'VOC' + curname, "Main")

    ext = '.jpg'
    img_files = get_ext_files(img_folder, ext)

    ext = '.txt'
    res_files = get_ext_files(result_folder, ext)

    # print img_files
    # print res_files

    for imgname in img_files:

        if '0000103_v3_test_11.jpg' != imgname:
            print imgname
            continue


        org_img = Image.open(os.path.join(img_folder, imgname))
        org_anno = os.path.join(anno_folder, imgname.split(".jpg")[ 0 ] + ".xml")

        names, xx0, yy0, xx1, yy1 = parse_annotation(org_anno)


        newnames = []
        newxx0 = []
        newyy0 = []
        newxx1 = []
        newyy1 = []
        conf = []

        for each_res_file in res_files:
            res_cls = each_res_file.split('trainval_')[ 1 ].split('.txt')[ 0 ]

            reader = open(os.path.join(result_folder, each_res_file), 'r')

            while 1:
                line = reader.readline()

                if not line:
                    break

                strs = line.split(" ")
                # print cmp(strs[ 0 ], imgname.split(".jpg")[ 0 ]), strs[ 0 ], imgname.split(".jpg")[ 0 ]
                if not cmp(strs[ 0 ], imgname.split(".jpg")[ 0 ]):

                    newnames.append(res_cls)
                    conf.append(float(strs[ 1 ]))
                    newxx0.append(float(strs[ 2 ]))
                    newyy0.append(float(strs[ 3 ]))
                    newxx1.append(float(strs[ 4 ]))
                    newyy1.append(float(strs[ 5 ]))

        fig = plt.subplots(nrows=2)  
        mngr = plt.get_current_fig_manager()
        # to put it into the upper left corner for example:
        # mngr.window.setGeometry(50,100,640, 545)

        plt.subplot(1,2,1)
        plt.title("gt: " + imgname)
        plt.imshow(org_img)

        currentAxis = plt.gca()

        for i in range(len(xx0)):
            pltcolor = get_color_list(names[ i ])
            currentAxis.add_patch(Rectangle((xx0[ i ], yy0[ i ]), xx1[ i ] - xx0[ i ], yy1[ i ] - yy0[ i ], alpha=0.2, color = pltcolor))

        plt.subplot(1,2,2)

        plt.title("dt")
        plt.imshow(org_img)
        currentAxis = plt.gca()
        for i in range(len(newxx0)):

            if conf[ i ] > 0.7:
                pltcolor = get_color_list(newnames[ i ])
                currentAxis.add_patch(Rectangle((newxx0[ i ], newyy0[ i ]), newxx1[ i ] - newxx0[ i ], newyy1[ i ] - newyy0[ i ], alpha=0.2, color = pltcolor))        
                currentAxis.text(newxx0[ i ], newyy0[ i ], "conf: " + str(conf[ i ]), fontsize = 4)
        
        plt.show()
    # print xx0, yy0, xx1, yy1  



def plot_compare_result_with_both(src_path_1, src_path_2):
    curname_1 = src_path_1.split('VOCdevkit')[ 1 ]
    img_folder_1 = os.path.join(src_path_1, 'VOC' + curname_1, "JPEGImages")
    anno_folder_1 = os.path.join(src_path_1, 'VOC' + curname_1, "Annotations")
    result_folder_1 = os.path.join(src_path_1, "results", 'VOC' + curname_1, "Main")

    ext = '.jpg'
    img_files_1 = get_ext_files(img_folder_1, ext)

    ext = '.txt'
    res_files_1 = get_ext_files(result_folder_1, ext)

    curname_2 = src_path_2.split('VOCdevkit')[ 1 ]
    img_folder_2 = os.path.join(src_path_2, 'VOC' + curname_2, "JPEGImages")
    anno_folder_2 = os.path.join(src_path_2, 'VOC' + curname_2, "Annotations")
    result_folder_2 = os.path.join(src_path_2, "results", 'VOC' + curname_2, "Main")

    ext = '.jpg'
    img_files_2 = get_ext_files(img_folder_2, ext)

    ext = '.txt'
    res_files_2 = get_ext_files(result_folder_2, ext)

    for imgname in img_files_1:
        org_img = Image.open(os.path.join(img_folder_1, imgname))
        org_anno = os.path.join(anno_folder_1, imgname.split(".jpg")[ 0 ] + ".xml")

        names, xx0, yy0, xx1, yy1 = parse_annotation(org_anno)

        newnames_1 = []
        newxx0_1 = []
        newyy0_1 = []
        newxx1_1 = []
        newyy1_1 = []
        conf_1 = []

        for each_res_file in res_files_1:
            res_cls = each_res_file.split('trainval_')[ 1 ].split('.txt')[ 0 ]

            reader = open(os.path.join(result_folder_1, each_res_file), 'r')

            while 1:
                line = reader.readline()

                if not line:
                    break

                strs = line.split(" ")
                # print cmp(strs[ 0 ], imgname.split(".jpg")[ 0 ]), strs[ 0 ], imgname.split(".jpg")[ 0 ]
                if not cmp(strs[ 0 ], imgname.split(".jpg")[ 0 ]):

                    newnames_1.append(res_cls)
                    conf_1.append(float(strs[ 1 ]))
                    newxx0_1.append(float(strs[ 2 ]))
                    newyy0_1.append(float(strs[ 3 ]))
                    newxx1_1.append(float(strs[ 4 ]))
                    newyy1_1.append(float(strs[ 5 ]))


        newnames_2 = []
        newxx0_2 = []
        newyy0_2 = []
        newxx1_2 = []
        newyy1_2 = []
        conf_2 = []

        for each_res_file in res_files_2:
            res_cls = each_res_file.split('trainval_')[ 1 ].split('.txt')[ 0 ]

            reader = open(os.path.join(result_folder_2, each_res_file), 'r')

            while 1:
                line = reader.readline()

                if not line:
                    break

                strs = line.split(" ")
                # print cmp(strs[ 0 ], imgname.split(".jpg")[ 0 ]), strs[ 0 ], imgname.split(".jpg")[ 0 ]
                if not cmp(strs[ 0 ], imgname.split(".jpg")[ 0 ]):

                    newnames_2.append(res_cls)
                    conf_2.append(float(strs[ 1 ]))
                    newxx0_2.append(float(strs[ 2 ]))
                    newyy0_2.append(float(strs[ 3 ]))
                    newxx1_2.append(float(strs[ 4 ]))
                    newyy1_2.append(float(strs[ 5 ]))



        fig = plt.subplots(nrows=3,figsize=(70,20))  

        plt.subplot(1,3,1)
        plt.title("gt: " + imgname)
        plt.imshow(org_img)

        currentAxis = plt.gca()

        for i in range(len(xx0)):
            pltcolor = get_color_list(names[ i ])
            currentAxis.add_patch(Rectangle((xx0[ i ], yy0[ i ]), xx1[ i ] - xx0[ i ], yy1[ i ] - yy0[ i ], alpha=0.2, color = pltcolor))

        plt.subplot(1,3,2)

        plt.title("dt: " + "rfcn")
        plt.imshow(org_img)
        currentAxis = plt.gca()
        for i in range(len(newxx0_1)):

            if conf_1[ i ] > 0.5:
                pltcolor = get_color_list(newnames_1[ i ])
                currentAxis.add_patch(Rectangle((newxx0_1[ i ], newyy0_1[ i ]), newxx1_1[ i ] - newxx0_1[ i ], newyy1_1[ i ] - newyy0_1[ i ], alpha=0.2, color = pltcolor))        
                currentAxis.text(newxx0_1[ i ], newyy0_1[ i ], "conf: " + str(conf_1[ i ]), fontsize = 4)

        plt.subplot(1,3,3)

        plt.title("dt: " + "rcnn")
        plt.imshow(org_img)
        currentAxis = plt.gca()
        for i in range(len(newxx0_2)):

            if conf_2[ i ] > 0.5:
                pltcolor = get_color_list(newnames_2[ i ])
                currentAxis.add_patch(Rectangle((newxx0_2[ i ], newyy0_2[ i ]), newxx1_2[ i ] - newxx0_2[ i ], newyy1_2[ i ] - newyy0_2[ i ], alpha=0.2, color = pltcolor))        
                currentAxis.text(newxx0_2[ i ], newyy0_2[ i ], "conf: " + str(conf_2[ i ]), fontsize = 4)

        plt.show()
    # print xx0, yy0, xx1, yy1  




if __name__ == '__main__':
    flag = sys.argv[1]
    src_path1 = sys.argv[2]
    src_path2 = sys.argv[3]

    if not os.path.exists(src_path1):
        print "Error!"
        sys.exit(1)

    # if not os.path.exists(src_path2):
    #     print "Error!"
    #     sys.exit(1)

    # os.popen("rm ./dst_path_contain/*.rec")
    # dt_tagging(src_path1)
    # gt_tagging(src_path1)

    if int(flag) == 1:
        plot_compare_result_with_gt(src_path1)
    if int(flag) == 2:
        plot_compare_result_with_both(src_path1, src_path2)










