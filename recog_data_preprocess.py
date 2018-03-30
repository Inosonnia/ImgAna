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

def read_label_file(label_file):
	dst_type_list = []
	ret_list = []
	f = codecs.open(label_file, 'r', 'utf-8')
	lines = f.readlines()
	f.close()
	for line in lines:
		line = line.strip()
		items = line.split(" ")
		if len(items) == 5:
			items.insert(0, "a")		
		tp = items[-1]
		new_items = []
		new_items.append(" ".join(items[:-5]))
		new_items.extend(items[-5:])
		if len(dst_type_list) == 0:
			ret_list.append(new_items)
		elif tp in dst_type_list:
			ret_list.append(new_items)
	return ret_list


def extract_equation_crops(srcpath, dstpath, dst_list_file, file_ext = ".rea", random_count = 10, with_quality = False):
	'''
	Extracts equation figs within a single image.
	'''
	image_files = glob.glob(os.path.join(srcpath, "*.jpg"))
	
	fwriter = open(dst_list_file, "w")	

	idx = 1

	#for image_file in image_files[4148:]:
	for image_file in image_files[:]:
		idx += 1
		print "img idx: ", idx, image_file

		img_name = os.path.splitext(os.path.basename(image_file))[0]
		label_file = image_file.replace(".jpg", file_ext)
		if not os.path.exists(label_file):
			continue

		img = Image.open(image_file)
		width, height = img.size
		label_list = read_label_file(label_file)

		
		idx_2 = 0

		for label in label_list:
			val_gt = label[0]
			x1 = int(label[1])
			y1 = int(label[2])
			x2 = int(label[3])
			y2 = int(label[4])

			if file_ext == ".box":
				y1 = height - int(label[4])
				y2 = height - int(label[2])

			if len(val_gt) > 1 and len(val_gt) < 200:
				new_gt = val_gt.replace(" ", "")

				idx_1 = 0

				for i in range(random_count):
					new_x1 = x1 + random.randint(-10, 0)
					new_x2 = x2 + random.randint(0, 10)		

					new_y1 = y1 + random.randint(-5, 0)		
					new_y2 = y2 + random.randint(0, 5)	


					if new_x1 <= 0 or new_y1 <= 0 or new_x2 >= width or new_y2 >= height:
						continue					

					try:
						img_crop = img.crop((new_x1, new_y1, new_x2, new_y2))

						img_save_name = "img" + str(idx) + "_label" + str(idx_2) + "_rnd" + str(idx_1) + ".jpg"

						dst_file = os.path.join(dstpath, img_save_name)

						idx_1 += 1
						if with_quality == True:
							j_quality = random.randint(80, 180)
							img_crop.save(dst_file, 'JPEG', quality = j_quality)						
						else:
							img_crop.save(dst_file)

						fwriter.write(img_save_name + " " + new_gt + '\n')
					except:
						pass

			idx_2 += 1
	fwriter.close()



def recog_data_preprocess(srcpath, dstpath, flag = 0):

	random_count = 5
	with_quality = False
	file_ext = ".rec"

	dst_list_file = osp.join(dstpath, "recog_filelist.txt")				
	extract_equation_crops(srcpath, dstpath, dst_list_file, file_ext, random_count=random_count, with_quality = with_quality)

	# g_dst_type_list = []

	# g_valid_list = [str(i) for i in range(0, 10)]
	# g_valid_list.extend([string.lowercase[i] for i in range(0, 26)])
	# g_valid_list.extend([string.uppercase[i] for i in range(0, 26)])
	# g_valid_list.extend(['-', '_', '.'])


if __name__ == '__main__': 

    srcpath = sys.argv[1] 
    dstpath = sys.argv[2]
    flag = int(sys.argv[3])

    if not os.path.exists(srcpath):
        print "Input not exists!"
        sys.exit(1)

    if not os.path.exists(dstpath):
        os.mkdir(dstpath)    

    recog_data_preprocess(srcpath, dstpath, flag)



