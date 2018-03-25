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

from sklearn.cluster import KMeans


img = cv2.imread('gradient.png',0)
ret,thresh_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)


def SeeImgColor(filename): # check the img status / bbox status of a single img
    '''
    evalFlag: If evaluation result is needed
    '''
    with open(filename) as curImg:
        if not os.path.exists(filename):
            print "These does not exist such a img !"
            sys.exit(1)


    # image = Image.open(filename).convert('RGB')
    # imgsp = np.shape(image)

    # pixels = []


    img = cv2.imread(filename)
    GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  
    ret,thresh1=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)  
    ret,thresh2=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY_INV)  
    ret,thresh3=cv2.threshold(GrayImage,127,255,cv2.THRESH_TRUNC)  
    ret,thresh4=cv2.threshold(GrayImage,127,255,cv2.THRESH_TOZERO)  
    ret,thresh5=cv2.threshold(GrayImage,127,255,cv2.THRESH_TOZERO_INV)  
    titles = ['Gray Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']  
    images = [GrayImage, thresh1, thresh2, thresh3, thresh4, thresh5]  
    for i in xrange(6):  
       plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')  
       plt.title(titles[i])  
       plt.xticks([]),plt.yticks([])  
    plt.show()  
    # b,g,r = cv2.split(img)
    # img = cv2.merge([r,g,b])


    # ret,thresh_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

    # fig = plt.figure()
    # plt.imshow(thresh_img)
    # plt.show()

    # print imgsp

    # call = np.zeros([26, 26, 26])
    # for w in range(0, imgsp[ 1 ]):
    #     for h in range(0, imgsp[ 0 ]):  
    #         pixels.append(image.getpixel((w, h)))
    #         # pixel = image.getpixel((w, h))   
    # #         # print pixel
    #         call [ int(pixel[ 0 ] / 10), int(pixel[ 1 ] / 10), int(pixel[ 2 ] / 10) ] = call [ int(pixel[ 0 ] / 10), int(pixel[ 1 ] / 10), int(pixel[ 2 ] / 10) ] + 1

    # estimator = KMeans(n_clusters=10)#构造聚类器
    # estimator.fit(pixels)#聚类
    # label_pred = estimator.labels_ #获取聚类标签
    # centroids = estimator.cluster_centers_ #获取聚类中心
    # inertia = estimator.inertia_ # 获取聚类准则的总和

    # print label_pred, centroids, inertia


    # # print call
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')

    # ax.scatter(call[ 0 ], call[ 1 ], call[ 2 ], c = 'r', marker = 'o')
    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # # ax.set_zlabel('Z Label')

    # plt.show()


if __name__ == '__main__': 
    filepath = sys.argv[1]
    # sav_log = sys.argv[2]
    # ImgAna(filepath)
    SeeImgColor(filepath)
