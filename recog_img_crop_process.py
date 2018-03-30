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

	for i in range(1):
	# for i in range(len(lines)):
		curline = lines[ i ].split("\n")[ 0 ]

		curFileName = os.path.join(srcImgDir, curline)

		if not os.path.exists(curFileName):
			print curFileName + " not exist!"
			sys.exit(1)

		print "curFile: " + curFileName
		img = Image.open(curFileName)
		# img.show()

		img_center_x = np.shape(img)[ 0 ]
		img_center_y = np.shape(img)[ 1 ]
		oldcenter = [img_center_x / 2.0, img_center_y / 2.0]


		# a positive angle
		angle = random.randint(5, 15)
		rotatedImg1 = img.rotate(angle, expand=True)
		# print np.shape(rotatedImg1)
		# rotatedImg1.show()

		r1_center_x = np.shape(rotatedImg1)[ 0 ]
		r1_center_y = np.shape(rotatedImg1)[ 1 ]

		newcenter = [r1_center_x / 2.0, r1_center_y / 2.0]
		CropImgWithAngle(oldcenter, newcenter, angle, curFileName, img, rotatedImg1, srcImgDir, dstImgPath)

		# # a negative angle
		# angle = random.randint(-15, -5)
		# rotatedImg2 = img.rotate(angle, expand=True)
		# # print np.shape(rotatedImg2)
		# # rotatedImg2.show()

		# r2_center_x = np.shape(rotatedImg2)[ 0 ]
		# r2_center_y = np.shape(rotatedImg2)[ 1 ]

		# newcenter = [r2_center_x / 2.0, r2_center_y / 2.0]
		# CropImgWithAngle(oldcenter, newcenter, angle, curFileName, img, rotatedImg2, srcImgDir, dstImgPath)





def CropImgWithAngle(oldcenter, newcenter, angle, ImgName, orgImg, Img, srcImgDir, dstImgPath):
	print ImgName


	dstImgList = os.path.join(srcImgDir, os.path.splitext(os.path.basename(ImgName))[0] + ".rec")
	if not os.path.exists(dstImgList):
		print dstImgList + " not exist!"
		sys.exit(1)

	gt_file = open(dstImgList)
	gtlines = gt_file.readlines()

	lines = []
	for line in gtlines:
	    lines.append(line)


	for i in range(len(lines)):
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

		print xold, yold, xnew, ynew
		print (x0 - xold) * math.cos(float(angle) / 180 * math.pi), (y0 - yold) * math.sin(float(angle) / 180 * math.pi)

		# four vertex. Movement: 1. move the bbox according to the new center 2. rotation: (x0 - xold) * math.cos(float(angle) / 180 * math.pi) - (y0 - yold) * math.sin(float(angle) / 180 * math.pi) + xnew
		newx0 = (x0 - xold) * math.cos(float(angle) / 180 * math.pi) - (y0 - yold) * math.sin(float(angle) / 180 * math.pi) + xnew + (xnew - xold)
		newy0 = (x0 - xold) * math.sin(float(angle) / 180 * math.pi) + (y0 - yold) * math.cos(float(angle) / 180 * math.pi) + ynew + (ynew - yold)

		newx1 = (x1 - xold) * math.cos(float(angle) / 180 * math.pi) - (y1 - yold) * math.sin(float(angle) / 180 * math.pi) + xnew + (xnew - xold)
		newy1 = (x1 - xold) * math.sin(float(angle) / 180 * math.pi) + (y1 - yold) * math.cos(float(angle) / 180 * math.pi) + ynew + (ynew - yold)

		newx2 = (x1 - xold) * math.cos(float(angle) / 180 * math.pi) - (y0 - yold) * math.sin(float(angle) / 180 * math.pi) + xnew + (xnew - xold)
		newy2 = (x1 - xold) * math.sin(float(angle) / 180 * math.pi) + (y0 - yold) * math.cos(float(angle) / 180 * math.pi) + ynew + (ynew - yold)

		newx3 = (x0 - xold) * math.cos(float(angle) / 180 * math.pi) - (y1 - yold) * math.sin(float(angle) / 180 * math.pi) + xnew + (xnew - xold)
		newy3 = (x0 - xold) * math.sin(float(angle) / 180 * math.pi) + (y1 - yold) * math.cos(float(angle) / 180 * math.pi) + ynew + (ynew - yold)

		# newx0 = (x0 - x + newcenter[ 0 ] - x) * math.cos(float(angle) / 180 * math.pi) - (y0 - y + newcenter[ 1 ] - y) * math.sin(float(angle) / 180 * math.pi) + x
		# newy0 = (x0 - x + newcenter[ 0 ] - x) * math.sin(float(angle) / 180 * math.pi) + (y0 - y + newcenter[ 1 ] - y) * math.cos(float(angle) / 180 * math.pi) + y

		# newx1 = (x1 - x + newcenter[ 0 ] - x) * math.cos(float(angle) / 180 * math.pi) - (y1 - y + newcenter[ 1 ] - y) * math.sin(float(angle) / 180 * math.pi) + x 
		# newy1 = (x1 - x + newcenter[ 0 ] - x) * math.sin(float(angle) / 180 * math.pi) + (y1 - y + newcenter[ 1 ] - y) * math.cos(float(angle) / 180 * math.pi) + y 

		# newx2 = (x1 - x + newcenter[ 0 ] - x) * math.cos(float(angle) / 180 * math.pi) - (y0 - y + newcenter[ 1 ] - y) * math.sin(float(angle) / 180 * math.pi) + x
		# newy2 = (x1 - x + newcenter[ 0 ] - x) * math.sin(float(angle) / 180 * math.pi) + (y0 - y + newcenter[ 1 ] - y) * math.cos(float(angle) / 180 * math.pi) + y

		# newx3 = (x0 - x + newcenter[ 0 ] - x) * math.cos(float(angle) / 180 * math.pi) - (y1 - y + newcenter[ 1 ] - y) * math.sin(float(angle) / 180 * math.pi) + x
		# newy3 = (x0 - x + newcenter[ 0 ] - x) * math.sin(float(angle) / 180 * math.pi) + (y1 - y + newcenter[ 1 ] - y) * math.cos(float(angle) / 180 * math.pi) + y


		newxs = np.min([newx0, newx1, newx2, newx3])
		newys = np.min([newy0, newy1, newy2, newy3])

		newxe = np.max([newx0, newx1, newx2, newx3])
		newye = np.max([newy0, newy1, newy2, newy3])

		# newxs = int(newxs)
		# newxe = int(newxe)
		# newys = int(newys)
		# newye = int(newye)

		print newxs, newxe, newys, newye

		# org_img_crop = orgImg.crop((x0, y0, x1, y1))
		img_crop = Img.crop((newxs, newys, newxe, newye))

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
