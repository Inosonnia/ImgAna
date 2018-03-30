#coding=utf-8  
import os, glob
import sys
import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
import numpy as np
import string
import random
import time
import uuid
import shutil 
import operator
import cv2  
import numpy as np  
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

class Box(object):
    def __init__(self,val=("",0,0,0,0,0)):
        self.content = val[0]
        self.xmin = val[1]
        self.ymin = val[2]
        self.xmax = val[3]
        self.ymax = val[4]
        self.label = val[5]
        self.w = self.xmax - self.xmin
        self.h = self.ymax - self.ymin
        
    def outStr(self):
        return '%s %d %d %d %d %d \n'%(self.content, self.xmin, self.ymin, self.xmax, self.ymax, self.label)
    
    def getContent(self):
        return '%s\n'%(self.content)

    def right():
        return self.xmax

    def bottom():
        return self.ymax
    
    def area(self):
        return self.w*self.h
    
    def __str__(self):
        return '%f,%f,%f,%f'%(self.xmin,self.ymin,self.xmin+self.w,self.ymin+self.h)

    def union(self,other):
        if self.area() == 0:
            return other
        if other.area() == 0:
            return self
        ix1 = min(self.xmin, other.xmin)
        iy1 = min(self.ymin, other.ymin)
        ix2 = max(self.xmin + self.w, other.xmin + other.w)
        iy2 = max(self.ymin + self.h, other.ymin + other.h) 
        return Box(('',ix1, iy1, ix2, iy2, 0))

    def intersection(self, other):
        ix1 = max(self.xmin, other.xmin)
        iy1 = max(self.ymin, other.ymin)
        ix2 = min(self.xmin + self.w, other.xmin + other.w)
        iy2 = min(self.ymin + self.h, other.ymin + other.h)
        if ix1 >= ix2 or iy1 >= iy2:
            return Box()
        return Box(('',ix1, iy1, ix2, iy2, 0))
    
    def iou(self, other):
        inter = self.intersection(other)
        return inter.area() * 1. / (self.area() + other.area() - inter.area())

    def inside(self, other):
        inter = self.intersection(other)
        return inter.area() * 1. / self.area()

def writeBoxesToFile(filePath, boxes, tp):
    lines = []
    for box in boxes:
        lines.append(box.outStr())
    file_object = open(filePath, tp)
    file_object.writelines(lines)
    file_object.close( )


def file_extension(path): 
    return os.path.splitext(path)[1] 

def file_name(path): 
    return os.path.splitext(path)[0] 

def get_ext_files(targdir, ext):
    return filter(lambda x: x.endswith(ext), os.listdir(targdir))

def copy_file_to(srcDir, targdir, fname):
    filepath = os.path.join(srcDir, fname + '.jpg')
    dstpath = os.path.join(targdir, fname + '.jpg')
    shutil.copyfile(filepath, dstpath)

def ImgCrop(filepath, dstpath, crop_num):

    if not os.path.exists(dstpath):
        os.mkdir(dstpath)

    for fname in get_ext_files(filepath, '.jpg'): # only support jpg

        ########### process the img ###########
        if not os.path.exists(os.path.join(filepath, file_name(fname) + '.jpg')):
            print "These does not exist such a img !"
            sys.exit(1)

        image = Image.open(os.path.join(filepath, file_name(fname) + '.jpg')).convert('RGB')
        imgsp = np.shape(image)

        # print imgsp
        img_width = imgsp[ 0 ]
        img_height = imgsp[ 1 ]

        gt_file = open(os.path.join(filepath, file_name(fname) + '.rec'))
        gtlines = gt_file.readlines()


        count = 0

        for line in gtlines:
            # print line
            words = line.strip().split(' ')
            wordsLen = len(words)
            
            if wordsLen < 6:
                print "Error annotation in " + fname
                sys.exit(1)
            
            content = " ".join(i for i in words[:-5])
            xmin = int(words[-5])
            xmax = int(words[-3])
            ymin = int(words[-4])
            ymax = int(words[-2])
            label = int(words[-1])

            bboxwidth = xmax - xmin
            bboxheight = ymax - ymin
            bboxcenterx = xmin + (xmax - xmin) / 2
            bboxcentery = ymin + (ymax - ymin) / 2


            if bboxheight <= 32: # 32 -- a threshold to determine if the box is small

                count = count + 1
                crop_ratio = round(random.uniform(0.25, 0.5), 2)

                newimgwidth = crop_ratio * img_width
                newimgheight = crop_ratio * img_height

                # print "img size: ", newimgwidth, newimgheight
                # print "bboxcenter: ", bboxcenterx, bboxcentery
                newx1 = bboxcenterx - newimgwidth / 2
                newx2 = bboxcenterx + newimgwidth / 2
                newy1 = bboxcentery - newimgheight / 2
                newy2 = bboxcentery + newimgheight / 2

                if newx1 < 0:
                    newx2 = newx2 - newx1
                    newx1 = 0
                    
                elif newx2 > imgsp[ 0 ]:
                    newx1 = newx1 - newx2 + imgsp[ 0 ]
                    newx2 = imgsp[ 0 ]

                if newy1 < 0:
                    newy2 = newy2 - newy1
                    newy1 = 0
                    
                elif newy2 > imgsp[ 1 ]:
                    newy1 = newy1 - newy2 + imgsp[ 1 ]
                    newy2 = imgsp[ 1 ]
                    
                ########### process the rec file ###########
                allBox = Box(('', 0, 0, newx2 - newx1, newy2 - newy1, 0))

                finxmin = []
                finxmax = []
                finymin = []
                finymax = []   
                finlabel = []  

                saveflag = 1
                for line in gtlines:

                    words = line.strip().split(' ')
                    if len(words) < 6:
                        continue

                    xmin = int(words[-5]) - newx1
                    xmax = int(words[-3]) - newx1
                    ymin = int(words[-4]) - newy1
                    ymax = int(words[-2]) - newy1
                    label = int(words[-1])

                    curBox = Box(('', xmin, ymin, xmax, ymax, 0))

                    # if curBox.inside(allBox) == 1: # the training set should not contain parts of equations
                    if curBox.inside(allBox) >= 0.7: # the training set should not contain parts of equations
                        finxmin.append(np.maximum(xmin, 0))
                        finxmax.append(np.minimum(xmax, newx2 - newx1))
                        finymin.append(np.maximum(ymin, 0))
                        finymax.append(np.minimum(ymax, newy2 - newy1))
                        finlabel.append(label)
                    else:
                        continue
                        # saveflag = 0
                        # break # does not wish to include the incomplete equations

                if len(finlabel) > 0:
                    save_name = os.path.join(dstpath, file_name(fname) + '_' + str(count) + '_crop_' + str(crop_ratio) + '.jpg')
                    new_img = image.crop([newx1, newy1, newx2, newy2]).convert('RGB').save(save_name)
                    save_anno = os.path.join(dstpath, os.path.splitext(os.path.basename(save_name))[0] + '.rec')
                    writer = open(save_anno, 'w')

                    for i in range(len(finxmin)):
                        writer.write('{0} {1} {2} {3} {4} {5}\n'.format("0", int(finxmin[ i ]), int(finymin[ i ]), int(finxmax[ i ]), int(finymax[ i ]), finlabel[ i ]))


                # print fname
                # sys.exit(0)


if __name__ == '__main__':
    filepath = sys.argv[1]
    dstpath = sys.argv[2]

    crop_num = 2 # select 2 from [0.5, 0.75]

    ImgCrop(filepath, dstpath, crop_num)














