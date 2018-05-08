#coding=utf-8  
import os, glob
import sys
import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import string
import random
import time
import uuid
import shutil 
import operator
import cv2  

import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg

from sklearn.cluster import KMeans
from sklearn.externals import joblib

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


def SeeAnchorScale(bboxWidth, bboxHeight, bboxScaleRatio):

    s1 = KMeans(n_clusters=3, random_state=0).fit(np.array(bboxWidth).reshape(-1, 1))
    s2 = KMeans(n_clusters=3, random_state=0).fit(np.array(bboxHeight).reshape(-1, 1))
    s3 = KMeans(n_clusters=3, random_state=0).fit(np.array(bboxScaleRatio).reshape(-1, 1))

    print s1.cluster_centers_, s2.cluster_centers_, s3.cluster_centers_


def CheckLegality(filepath, filename):
    if not os.path.exists(os.path.join(filepath, filename)):
        print "These does not exist such a file !"
        sys.exit(1)

def ImgAna(filepath):

    imgWidth = []
    imgHeight = []
    for fname in get_ext_files(filepath, '.jpg'): # only support jpg
        CheckLegality(filepath, file_name(fname) + '.jpg')

        image = Image.open(os.path.join(filepath, file_name(fname) + '.jpg')).convert('RGB')

        imgsp = np.shape(image)
        imgWidth.append(imgsp[ 0 ])
        imgHeight.append(imgsp[ 1 ])

    print np.shape(imgWidth)

    plt.figure(1)
    plt.scatter(imgWidth, imgHeight)
    plt.title("Image size distribution")
    plt.xlabel("Image width (Unit: pixel)")
    plt.ylabel("Image height (Unit: pixel)")
    plt.xlim(0, 2000)
    plt.ylim(0, 2000)
    plt.legend(loc = 'upper right')
    # plt.show()

    plt.savefig('ImgInfo.pdf',dpi=150)
    # print imgWidth, imgHeight
    # image.show() 

def BboxAna(filepath):

    bboxWidth = []
    bboxHeight = []
    bboxCenterx = []
    bboxCentery = []
    bboxScaleRatio = []

    height_count = {}

    for fname in get_ext_files(filepath, '.rec'): # only support jpg
        if not os.path.exists(os.path.join(filepath, file_name(fname) + '.rec')):
            print "These does not exist such a img annotation !"
            sys.exit(1)

        gt_file = open(os.path.join(filepath, file_name(fname) + '.rec'))
        gtlines = gt_file.readlines()
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
            bboxcenterx = (xmax - xmin) / 2
            bboxcentery = (ymax - ymin) / 2
            bboxscaleratio = float(bboxheight) / float(bboxwidth)

            bboxWidth.append(bboxwidth)
            bboxHeight.append(bboxheight)
            bboxCenterx.append(bboxcenterx)
            bboxCentery.append(bboxcentery)
            bboxScaleRatio.append(bboxscaleratio)

            bbox_height_scale = bboxheight / 16

            if bbox_height_scale not in height_count:
                height_count [ bbox_height_scale ] = 1
            else:
                height_count[ bbox_height_scale ] = height_count[ bbox_height_scale ] + 1                

    print "Height scale distribution: ", height_count


    SeeAnchorScale(bboxWidth, bboxHeight, bboxScaleRatio)
    # fig,(ax0, ax1) = plt.subplots(nrows=2)  
    # plt.subplots(nrows=3,figsize=(9,6)) 




    # plt.figure(2)
    # plt.scatter(bboxWidth, bboxHeight)
    # plt.title("bbox size distribution")
    # plt.xlabel("bbox width (Unit: pixel)")
    # plt.ylabel("bbox height (Unit: pixel)")
    # plt.xlim(0, 2000)
    # plt.ylim(0, 2000)
    # plt.legend(loc = 'upper right')
    # plt.savefig('BboxSizeInfo.pdf',dpi=150)

    # plt.figure(3)
    # plt.scatter(bboxCenterx, bboxCentery)
    # plt.title("bbox center distribution")
    # plt.xlabel("bbox center location (Unit: pixel)")
    # plt.ylabel("bbox center location (Unit: pixel)")
    # plt.xlim(0, 1000)
    # plt.ylim(0, 1000)
    # # plt.show()
    # plt.legend(loc = 'upper right')
    # plt.savefig('BboxCenterInfo.pdf',dpi=150)

    # plt.figure(4)
    # # plt.hist(height_count,20,normed=1,histtype='bar',facecolor='yellowgreen',alpha=0.75)  
    # plt.hist(bboxScaleRatio,40,normed=1,histtype='bar',facecolor='yellowgreen',alpha=0.75)  
    # plt.title("bbox scale distribution")
    # plt.xlabel("bbox width (Unit: pixel)")
    # plt.ylabel("bbox height (Unit: pixel)")
    # # plt.xlim(0, 4000)
    # # plt.ylim(0, 3000)
    # plt.legend(loc = 'upper right')
    # # plt.show()
    # plt.savefig('BboxScaleInfo.pdf',dpi=150)





def ErrorAna(filepath, sav_log):
    writer = open(sav_log, 'w')
    height_count = {} # store the height distribution
    for fname in get_ext_files(filepath, '.rea'): # only support rea
        print "reading ", fname, ' ...'
        if not os.path.exists(os.path.join(filepath, file_name(fname) + '.rea')):
            print "These does not exist such a img error annotation !"
            sys.exit(1)

        gt_file = open(os.path.join(filepath, file_name(fname) + '.rea'))
        gtlines = gt_file.readlines()

        error_type = "Failed"

        for line in gtlines:
            # print line
            words = line.strip().split(' ')
            wordsLen = len(words)
            
            if wordsLen < 6:
                print "No error annotation in " + fname
                sys.exit(1)

            content = " ".join(i for i in words[:-5])
            xmin = int(words[-5])
            xmax = int(words[-3])
            ymin = int(words[-4])
            ymax = int(words[-2])
            label = int(words[-1])

            bboxwidth = xmax - xmin

            if bboxwidth == 0:
                error_type = "Missed"

            if bboxwidth != 0:
                bboxheight = ymax - ymin
                bboxcenterx = (xmax - xmin) / 2
                bboxcentery = (ymax - ymin) / 2
                bboxscaleratio = float(bboxwidth) / float(bboxheight)

                print fname, "bbox height: ", bboxheight, " label: ", label, " Error type: ", error_type
                
                writer.write(str(fname) + "bbox height: " + str(bboxheight) + " label: " + str(label) + " Error type: " + str(error_type) + '\n')

                bbox_height_scale = bboxheight / 16


                if bbox_height_scale not in height_count:
                    height_count [ bbox_height_scale ] = 1
                else:
                    height_count[ bbox_height_scale ] = height_count[ bbox_height_scale ] + 1                


    print "Err Height scale distribution: ", height_count

def WatchSingleImg(filename, evalFlag): # check the img status / bbox status of a single img
    '''
    evalFlag: If evaluation result is needed
    '''
    with open(filename) as curImg:
        if not os.path.exists(filename + '.jpg'):
            print "These does not exist such a img !"
            sys.exit(1)

    image = Image.open(filename + '.jpg').convert('RGB')
    imgsp = np.shape(image)
    imgWidth.append(imgsp[ 0 ])
    imgHeight.append(imgsp[ 1 ])


    if evalFlag == 1:
        get_error_box_result(filename)


def get_error_box_result(filename):
    # print fname
    # if fname == "v3_test_136.recc":
    #     pass
    # else:
    #     continue

    with open(filename) as rt_file:
        if not os.path.exists(filename):
            print "These does not exist such a img result !"
            sys.exit(1)

        gt_file = open(fname)
        gtlines = gt_file.readlines()
        rtlines = rt_file.readlines()

        gtboxes = []
        for line in gtlines:
            # print line
            words = line.strip().split(' ')
            wordsLen = len(words)
            
            if wordsLen < 6:
                continue
            
            content = " ".join(i for i in words[:-5])
            xmin = int(words[-5])
            xmax = int(words[-3])
            ymin = int(words[-4])
            ymax = int(words[-2])
            label = int(words[-1])
            gtboxes.append(Box((content, xmin, ymin, xmax, ymax, label)))

        rtboxes = []
        for line in rtlines:
            words = line.strip().split(' ')
            wordsLen = len(words)
            
            if wordsLen < 6:
                continue
            
            content = " ".join(i for i in words[:-5])
            xmin = int(words[-5])
            xmax = int(words[-3])
            ymin = int(words[-4])
            ymax = int(words[-2])
            label = int(words[-1])

            rtboxes.append(Box((content, xmin, ymin, xmax, ymax, label)))


        gtsize = np.shape(gtboxes)

        detect_failed_box = []
        detect_missed_box = []
        detect_missed_box_idx = np.zeros(gtsize[ 0 ])

        for rt in rtboxes:
            for idx, gt in zip(range(gtsize[ 0 ]), gtboxes):
                
                if rt.iou(gt) > 0.5:
                    detect_missed_box_idx[ idx ] = 1

                    if rt.label != gt.label:

                        detect_failed_box.append(rt)
                        break
        
        detect_missed_box.append(Box((" 0 ", 0, 0, 0, 0, 0)))
        for i in range(gtsize[ 0 ]):
            if detect_missed_box_idx[ i ] == 0: # a missed gt box
                detect_missed_box.append(gtboxes[ i ])

        print "------- Error Detect -------"
        for box in detect_failed_box:
            print box.outStr()

        print "------- Miss Detect -------"
        for box in detect_missed_box:
            print box.outStr()


if __name__ == '__main__':
    filepath = sys.argv[1]
    sav_log = sys.argv[2]
    ImgAna(filepath)
    # BboxAna(filepath)
    # ErrorAna(filepath, sav_log)















