#coding=utf-8  
import os
import shutil
import glob
from os import path as osp
import sys
from PIL import Image, ImageDraw
import random
import string
import codecs
import skimage.transform
import numpy as np
import math


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




def ProcessEachImgByRotation(srcImgDir, dstImgPath):
	'''
	Rotate each img by a certain degree range, save their names and gt

	dstImgPath: location to save the rotated img
	'''

	gt_file = open(srcImgDir + "filelist.txt")
	gtlines = gt_file.readlines()

	lines = []

	for line in gtlines:
	    lines.append(line)

	rotatedFileNames = []
	rotatedEquations = []

	# for i in range(1):
	for i in range(len(lines)):
		curline = lines[ i ].split("\n")[ 0 ]

		curFileName = os.path.join(srcImgDir, curline)

		if not os.path.exists(curFileName):
			print curFileName + " not exist!"
			sys.exit(1)

		print "curFile: " + curFileName
		img = Image.open(curFileName)
		print np.shape(img)
		# img.show()

		img_center_x = np.shape(img)[ 1 ]
		img_center_y = np.shape(img)[ 0 ]
		oldcenter = [img_center_x / 2.0, img_center_y / 2.0]

		# a positive angle
		angle = random.randint(5, 15)
		rotatedImg1 = img.rotate(angle, expand=True)
		# print np.shape(rotatedImg1)
		# rotatedImg1.show()
		# rotatedImg1.save(os.path.join(srcImgDir, '_angle_{0}_idx_{1}'.format(angle, i) + ".jpg"))	


		r1_center_x = np.shape(rotatedImg1)[ 1 ]
		r1_center_y = np.shape(rotatedImg1)[ 0 ]

		newcenter = [r1_center_x / 2.0, r1_center_y / 2.0]
		CropImgWithAngle(oldcenter, newcenter, angle, curFileName, img, rotatedImg1, srcImgDir, dstImgPath)

		# a negative angle
		angle = random.randint(-15, -5)
		rotatedImg2 = img.rotate(angle, expand=True)
		# print np.shape(rotatedImg2)
		# rotatedImg2.show()

		r2_center_x = np.shape(rotatedImg2)[ 1 ]
		r2_center_y = np.shape(rotatedImg2)[ 0 ]

		newcenter = [r2_center_x / 2.0, r2_center_y / 2.0]
		CropImgWithAngle(oldcenter, newcenter, angle, curFileName, img, rotatedImg2, srcImgDir, dstImgPath)
		# rotatedImg2.show()
		# rotatedImg2.save(os.path.join(srcImgDir, '_angle_{0}_idx_{1}'.format(angle, i) + ".jpg"))



def CheckOverlap(lines):

	igrLines = []
	allBox = []

	for i in range(len(lines)):
		curStr = lines[ i ].split(" ")

		x0 = int(curStr[ 1 ])
		y0 = int(curStr[ 2 ])
		x1 = int(curStr[ 3 ])
		y1 = int(curStr[ 4 ])

		allBox.append(Box((" 0 ", x0, y0, x1, y1, " 0 ")))

	for i in range(len(lines)):

		if i in igrLines:
			continue

		for j in range(i + 1, len(lines)):

			if j in igrLines:
				continue

			print i, j

			if allBox[ i ].iou(allBox[ j ]) > 0:
				igrLines.append(i)
				igrLines.append(j)


	return igrLines	




def CropImgWithAngle(oldcenter, newcenter, angle, ImgName, orgImg, newImg, srcImgDir, dstImgPath):
	print "Img name: ", ImgName

	dstImgList = os.path.join(srcImgDir, os.path.splitext(os.path.basename(ImgName))[0] + ".rec")
	if not os.path.exists(dstImgList):
		print dstImgList + " not exist!"
		sys.exit(1)

	gt_file = open(dstImgList)
	gtlines = gt_file.readlines()

	lines = []
	for line in gtlines:
	    lines.append(line)

	igrLines = []
	igrLines = CheckOverlap(lines)

	print igrLines
	for i in range(len(lines)):

		if i in igrLines: # this bbox overlaps with other bboxes, direct ignore 
			continue 

		curStr = lines[ i ].split(" ")
		content = curStr[ 0 ]
		x0 = int(curStr[ 1 ])
		y0 = int(curStr[ 2 ])
		x1 = int(curStr[ 3 ])
		y1 = int(curStr[ 4 ])

		xold = oldcenter[ 0 ] # img center before transform
		yold = oldcenter[ 1 ]

		xnew = newcenter[ 0 ] # img center after transform
		ynew = newcenter[ 1 ]

		# four vertex. Movement: 
		# 1. move the bbox according to the new center -- e.g.  : + (xnew - xold)
		# 2. rotation -- e.g. : (x0 - xcenter) * cos(theta) - (y0 - ycenter) * sin(theta) + xcenter
		x0 = x0 + xnew - xold
		y0 = y0 + ynew - yold
		x1 = x1 + xnew - xold
		y1 = y1 + ynew - yold

		angle_pi = - angle / 180.0 * math.pi

		# print (x0 - xnew) * math.cos(angle_pi), - (y0 - ynew) * math.sin(angle_pi)
		# print x0, xnew

		newx0 = (x0 - xnew) * math.cos(angle_pi) - (y0 - ynew) * math.sin(angle_pi) + xnew
		newy0 = (x0 - xnew) * math.sin(angle_pi) + (y0 - ynew) * math.cos(angle_pi) + ynew

		newx1 = (x1 - xnew) * math.cos(angle_pi) - (y1 - ynew) * math.sin(angle_pi) + xnew
		newy1 = (x1 - xnew) * math.sin(angle_pi) + (y1 - ynew) * math.cos(angle_pi) + ynew

		newx2 = (x1 - xnew) * math.cos(angle_pi) - (y0 - ynew) * math.sin(angle_pi) + xnew
		newy2 = (x1 - xnew) * math.sin(angle_pi) + (y0 - ynew) * math.cos(angle_pi) + ynew

		newx3 = (x0 - xnew) * math.cos(angle_pi) - (y1 - ynew) * math.sin(angle_pi) + xnew
		newy3 = (x0 - xnew) * math.sin(angle_pi) + (y1 - ynew) * math.cos(angle_pi) + ynew

		newxs = np.min([newx0, newx1, newx2, newx3])
		newys = np.min([newy0, newy1, newy2, newy3])

		newxe = np.max([newx0, newx1, newx2, newx3])
		newye = np.max([newy0, newy1, newy2, newy3])

		# print xold, yold, xnew, ynew
		# print "xrange: ", newx0, newx1, newx2, newx3
		# print "yrange: ", newy0, newy1, newy2, newy3
		# print newxs, newxe, newys, newye

		# org_img_crop = orgImg.crop((x0, y0, x1, y1))
		img_crop = newImg.crop((newxs, newys, newxe, newye))

		# org_img_crop.show()
		# img_crop.show()

		print "org_coord: ", x0,y0,x1,y1, "-------  center: ", xold, yold
		print "new_coord", newxs, newys, newxe, newye, "-------  center: ", xnew, ynew, "-------  shape: ", np.shape(img_crop)
		img_crop.save(os.path.join(dstImgPath, os.path.splitext(os.path.basename(ImgName))[0] + '_angle_{0}_idx_{1}'.format(angle, i) + ".jpg"))		
		print "Saving crop img: " + os.path.splitext(os.path.basename(ImgName))[0] + '_angle_{0}'.format(angle) + ".jpg"


def SaveNewAnnotation(rotatedFileNames, rotatedEquations, dstImgPath):
	dstImgList = os.path.join(dstImgPath, "filelist.txt")
	writer = open(dstImgList, 'w')

	for i in range(len(rotatedFileNames)):
		writer.write(rotatedFileNames[ i ] + " " + rotatedEquations[ i ] + "\n")

# def MergeMultipleDataSet():


if __name__ == '__main__': 

    srcImgDir = sys.argv[1] 
    dstImgPath = sys.argv[2]

    if not os.path.exists(srcImgDir):
        print "Input filelist not exists!"
        sys.exit(1)

    if not os.path.exists(dstImgPath):
        os.mkdir(dstImgPath)    

    ProcessEachImgByRotation(srcImgDir, dstImgPath)
    # SaveNewAnnotation(rotatedFileNames, rotatedEquations, dstImgPath)
