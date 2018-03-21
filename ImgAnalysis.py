#coding=utf-8  
import os, glob
import sys
import commands
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import string
import random
import time
import uuid
import shutil 
import operator
import cv2  
import numpy as np  

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



def ImgAna(filepath):
    for fname in get_ext_files(filepath, '.jpg'): # only support jpg



def BboxAna(filepath):



if __name__ == '__main__':
    filepath = sys.argv[1]
    ImgAna(filepath)
    # BboxAna(filepath)















