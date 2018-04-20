#coding=utf-8  
import os, glob
import sys
import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter
#import matplotlib.pyplot as plt
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
    filepath = os.path.join(srcDir, fname)

    if '/' in fname:
        print fname
        fname = fname.replace('/', '_')

    dstpath = os.path.join(targdir, fname)

    print filepath, dstpath
    shutil.copyfile(filepath, dstpath)

def download_img_samples(filelist, dstpath):

    train_list = open(filelist, 'r')
    gtlines = train_list.readlines()    

    for line in gtlines:
        # print line
        S = line.strip().split(' = ') # line example: data000216 = /data1/home/rexyuan/train_set/handwrite/line_data/all_list_hsbc_digital.txt
        filename = S[ 1 ]

        tmp = S[1].split('/')[:-1]

        srcDir = ""
        for i in range(len(tmp)):
            srcDir = srcDir + tmp[ i ] + '/'
        # print "filename: ", filename, "srcDir: ", srcDir

        newfoldername = S[ 0 ]

        outdir = os.path.join(dstpath, newfoldername)

        if not os.path.exists(outdir):
            os.mkdir(outdir)

        newfilelist = open(os.path.join(outdir, "filelist.txt"), 'w')

        cur_data_list = open(filename, 'r')
        cur_data_lines = cur_data_list.readlines()   # cur_data_lines example: 3417_rename_correct_7/18666868751_1190_1.jpg 1,8,6,6,6,8,6,8,7,5,1

        seeds = [random.randint(0, len(cur_data_lines)) for _ in range(100)]
        # print "seeds: ", seeds

        alllines = []
        for cur_line, idx in zip(cur_data_lines, range(len(cur_data_lines))):
            # print "cur_line, idx: ", cur_line, idx

            if idx in seeds:
                S = cur_line.strip().split(' ')

                imgname = S[ 0 ]
                label = S[ 1 ]

                alllines.append(cur_line)
                copy_file_to(srcDir, outdir, imgname)
            else:
                continue

        sorted_lines = np.sort(alllines)
        for cur_line in sorted_lines:
            newfilelist.writelines(cur_line)

        newfilelist.close()


def read_tag_file(tag_file):
    file_io = codecs.open(tag_file,'r','utf-8')
    lines = file_io.readlines()
    file_io.close()
    tag_map = {}

    for line in lines:
        line = line.strip()  
        label,text = line.split()
        label = label.split(',')[0]
        text  = text.split(',')[0]

        tag_map[label] = text
        # tag_map[label] = text.encode("ascii","ignore")
    return tag_map


def label2txt(tag_file, label_file, output_file):

    tag_map = read_tag_file(tag_file)

    file_io = codecs.open(label_file,'r','utf-8')
    lines = file_io.readlines()
    file_io.close() 

    ignore_lines = []
    file_io = codecs.open(output_file, 'w','utf-8')

    # print tag_map

    for line in lines:
        line = line.strip()  
        print line
        path, text = line.split() 

        # print text
        tag_maps = ""
        for ch in text.split(','):
            if tag_map.has_key(ch):
                # print ch,tag_map[ch]
                tag_maps = tag_maps + '%s' %(tag_map[ch])

        # tag_maps = tag_maps.encode('utf-8')
        file_io.write('%s %s\n' %(path, tag_maps))

if __name__ == '__main__':
    '''
    Download img samples from training list, in order to avoid training error
    '''
    filelist = sys.argv[1]
    dstpath = sys.argv[2]

    if not os.path.exists(dstpath):
        os.mkdir(dstpath)

    download_img_samples(filelist, dstpath)

    train_list = open(filelist, 'r')
    gtlines = train_list.readlines()    

    for line in gtlines:
        # print line
        S = line.strip().split(' = ') # line example: data000216 = /data1/home/rexyuan/train_set/handwrite/line_data/all_list_hsbc_digital.txt
        newfoldername = S[ 0 ]

        outdir = os.path.join(dstpath, newfoldername)

        label_file = os.path.join(outdir, "filelist.txt")
        tag_file = os.path.join(dstpath, "gtlabel.txt")
        output_file = os.path.join(outdir, "filelist_coded.txt")

        label2txt(tag_file, label_file, output_file)




















