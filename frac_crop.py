#!/bin/env python
#coding:utf-8
import glob
import sys
import os
import shutil
import random

from PIL import Image
import numpy as np

def get_ext_files(targdir, ext):
    return filter(lambda x: x.endswith(ext), os.listdir(targdir))

def rename_files(dstpath, prefix, ext):
    files = get_ext_files(dstpath, ext)
    files.sort()
    count = 1
    # print dstpath
    for file in files:
        print "rename " + dstpath + file + " to -->: " + dstpath + prefix + str(count) + ext
        os.rename(dstpath + file, dstpath + prefix + str(count) + ext)
        count = count + 1

def frac_crop(src_path, dst_path):
    ext = ".rec"
    files = get_ext_files(src_path, ext)

    # for i in range(1):
    for i in range(len(files)):
        # file = open(os.path.join(dst_path, files[ i ]), 'w')

        frac_file = open(os.path.join(src_path, files[ i ]), 'r')
        print os.path.join(src_path, files[ i ])
           
        frac_bbox = []    
        main_bbox = []

        while 1:
            line = frac_file.readline()

            print line
            coords = line.split(" ")

            x1 = int( coords[ 1 ] )
            y1 = int( coords[ 2 ] )
            x2 = int( coords[ 3 ] )
            y2 = int( coords[ 4 ] )
            b_class = int( coords[ 5 ] ) 

            if not line:
                break

            if b_class == 0:
                frac_bbox.append(line)
            else:
                main_bbox.append(line)
        # print frac_bbox, main_bbox



        for j in range(len(main_bbox)): 

            curbbox = main_bbox[ j ].split(" ")

            big_x1 = int( curbbox[ 1 ] )
            big_y1 = int( curbbox[ 2 ] )
            big_x2 = int( curbbox[ 3 ] )
            big_y2 = int( curbbox[ 4 ] )
            big_class = int( curbbox[ 5 ] ) 
            big_box = [big_x1, big_y1, big_x2, big_y2]

            frac_components = []

            for k in range(len(frac_bbox)):

                curfracbbox = frac_bbox[ k ].split(" ")

                x1 = int( curfracbbox[ 1 ] )
                y1 = int( curfracbbox[ 2 ] )
                x2 = int( curfracbbox[ 3 ] )
                y2 = int( curfracbbox[ 4 ] )
                b_class = int( curfracbbox[ 5 ] )   
                small_box = [x1, y1, x2, y2]

                area_small = (x2 - x1 + 1) * (y2 - y1 + 1)

                xx1 = np.maximum(x1, big_x1)
                yy1 = np.maximum(y1, big_y1)
                xx2 = np.minimum(x2, big_x2)
                yy2 = np.minimum(y2, big_y2) 
                
                w = np.maximum(0.0, xx2 - xx1 + 1)
                h = np.maximum(0.0, yy2 - yy1 + 1)
                inter = w * h

                if inter / area_small > 0.9: # almost in the big rectangle 
                    frac_components.append(x1 + " " + y1 + " " + x2 + " " + y2 + "\n")

            print "frac_components, ", frac_components

            img_name = files[ i ].split(".rec")[ 0 ]
            crop_img_and_renew_rec( frac_components, big_box, img_name, j, src_path, dst_path )


def crop_img_and_renew_rec( frac_components, big_box, img_name, count, src_path, dst_path ):
    org_img = Image.open(os.path.join(src_path, img_name + ".jpg"))

    save_img_name = os.path.join(dst_path, '{0}_crop_{1}.jpg'.format(img_name, count))

    x0 = big_box[ 0 ]
    y0 = big_box[ 1 ]
    x1 = big_box[ 2 ]
    y1 = big_box[ 3 ]

    image.crop((x0, y0, x1, y1)).save(save_img_name)

    save_rec_name = os.path.join(dst_path, '{0}_crop_{1}.rec'.format(img_name, count))
    writer = open(save_rec_name, 'w')

    for i in range(len(frac_components)):
        x_min = frac_components[ 0 ] - big_box[ 0 ]
        x_max = frac_components[ 2 ] - big_box[ 0 ]
        y_min = frac_components[ 1 ] - big_box[ 1 ]
        y_max = frac_components[ 3 ] - big_box[ 1 ]

        writer.write('{0} {1} {2} {3} {4} {5}\n'.format("0", x_min, y_min, x_max, y_max, "100"))



if __name__ == '__main__':
    src_path = sys.argv[1]
    dst_path = sys.argv[2]

    if not os.path.exists(dst_path):
        os.mkdir(dst_path)

    # os.popen("rm ./dst_path_contain/*.rec")
    frac_crop(src_path, dst_path)










