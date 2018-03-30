#coding=utf-8  
import os, glob
import sys
import cv2  
import numpy as np 
import matplotlib.pyplot as plt

def file_extension(path): 
    return os.path.splitext(path)[1] 

def file_name(path): 
    return os.path.splitext(path)[0] 

def get_ext_files(targdir, ext):
    return filter(lambda x: x.endswith(ext), os.listdir(targdir))

def SeeImgColor(srcpath, dstpath):

    for fname in get_ext_files(srcpath, '.jpg'): # only support jpg
        if not os.path.exists(os.path.join(srcpath, file_name(fname) + '.jpg')):
            print "These does not exist such a img !"
            sys.exit(1)

        img = cv2.imread(os.path.join(srcpath, file_name(fname) + '.jpg'))

        width = np.shape(img)[ 0 ]
        height = np.shape(img)[ 1 ]
        GrayImage=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  
        # ret,thresh1=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY)  
        ret,thresh2=cv2.threshold(GrayImage,127,255,cv2.THRESH_BINARY_INV)  
        # ret,thresh3=cv2.threshold(GrayImage,127,255,cv2.THRESH_TRUNC)  
        # ret,thresh4=cv2.threshold(GrayImage,127,255,cv2.THRESH_TOZERO)  
        # ret,thresh5=cv2.threshold(GrayImage,127,255,cv2.THRESH_TOZERO_INV)  

        print np.shape(thresh2)
        fig = plt.figure(frameon=False)
        fig.set_size_inches(height, width)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(thresh2, aspect='normal')
        fig.savefig(os.path.join(dstpath, file_name(fname) + '.jpg'), dpi=1)


        # plt.figure(figsize = (width / 100, height / 100), dpi = 100)
        # plt.imshow(thresh2, 'gray')
        # plt.show()
        # plt.savefig(os.path.join(dstpath, file_name(fname) + '.jpg'))
        # plt.close()
        # titles = ['Gray Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']  
        # images = [GrayImage, thresh1, thresh2, thresh3, thresh4, thresh5]  
        # for i in xrange(6):  
        #    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')  
        #    plt.title(titles[i])  
        #    plt.xticks([]),plt.yticks([])  
        # plt.show()  

if __name__ == '__main__': 
    srcpath = sys.argv[1]
    dstpath = sys.argv[2]

    if not os.path.exists(dstpath):
        os.mkdir(dstpath)    
    # ImgAna(srcpath)
    SeeImgColor(srcpath, dstpath)
