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

g_dst_type_list = []

g_valid_list = [str(i) for i in range(0, 10)]
g_valid_list.extend([string.lowercase[i] for i in range(0, 26)])
g_valid_list.extend([string.uppercase[i] for i in range(0, 26)])
g_valid_list.extend(['-', '_', '.'])

#print g_valid_list

def mkdir(p):
	if not os.path.exists(p):
		os.mkdir(p)

def box_area(box):
    return (box[2] - box[0]) * (box[3] - box[1])

def box_intersection(box1, box2):
    ix1 = max(box1[0], box2[0])
    iy1 = max(box1[1], box2[1])
    ix2 = min(box1[2], box2[2])
    iy2 = min(box1[3], box2[3])
    if ix1 >= ix2 or iy1 >= iy2:
        return (0, 0, 0, 0)
    return (ix1,iy1,ix2,iy2)

def read_label_file(label_file):
	dst_type_list = ['103', '203']
	dst_type_list = g_dst_type_list
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

		idx_1 = 0
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

				for i in range(random_count):
					new_x1 = x1 + random.randint(-10, 0)
					new_x2 = x2 + random.randint(0, 10)		

					new_y1 = y1 + random.randint(-5, 0)		
					new_y2 = y2 + random.randint(0, 5)	


					if new_x1 <= 0 or new_y1 <= 0 or (new_x2) >= width or (new_y2) >= height:
						continue					

					try:
						img_crop = img.crop((new_x1, new_y1, new_x2, new_y2))

						img_save_name = "img" + str(idx) + "_label" + str(idx_2) + "_rnd" + str(idx_1) + ".jpg"

						dst_file = os.path.join(dstpath, img_save_name)

						idx_1 += 1
						if with_quality == True:
							j_quality = random.randint(30, 80)
							img_crop.save(dst_file, 'JPEG', quality = j_quality)						
						else:
							img_crop.save(dst_file)

						fwriter.write(img_save_name + " " + new_gt + '\n')
					except:
						pass

			idx_2 += 1
	fwriter.close()



def box_padding(box, x, y):
	new_box = list(box)
	new_box[0] = box[0] - x
	new_box[1] = box[1] - y
	new_box[2] = box[2] + x
	new_box[3] = box[3] + y
	return new_box

g_number_list = [str(i) for i in range(10)]

def gen_data_list(image_dir):
	image_files = glob.glob(os.path.join(image_dir, "*.jpg"))
	img_dict = {}
	for f in image_files:
		bname = osp.basename(f)
		pref, label = bname.split("_")[:2]
		print pref, label
	# 	if pref not in img_dict.keys():
	# 		img_dict[pref] = []
	# 	img_dict[pref].append(bname + " " + label)
	# for k, v in img_dict.iteritems():
	# 	dst_file = osp.join(image_dir, k + "_list.txt")
	# 	open(dst_file, "w").write('\n'.join(v))


def extract_valid_images(srcpath, dstpath, data_list, dst_data_list, driver = False):
	#mkdir(dstpath)
	lines = open(data_list, 'r').readlines()

	dst_lines = []
	for line in lines:
		line = line.strip()
		items = line.split(" ")
		fname = osp.join(srcpath, items[0])
		bname = osp.basename(fname)
		if driver == True:
			if bname.startswith("5_") and "_dr_" in bname:
				continue
			if bname.startswith("4_") and "_dr_" not in bname:
				continue
		width = 0
		try:
			img = Image.open(fname)
			width, height = img.size
		except:
			pass
		if width == 0:
			continue
		ratio = width * 1.0 / height
		if ratio < 8 and ratio > 0.8:
			dst_lines.append(line)

	open(dst_data_list, "w").write('\n'.join(dst_lines))


def extract_badcase(src_dir, dst_dir, err_file):
	mkdir(dst_dir)
	lines = open(err_file, 'r').readlines()
	for line in lines:
		line = line.strip()
		file_name, gt, val = line.split(",")
		file_name = file_name.strip()
		gt = gt.strip()
		val = val.strip()
		val = val.replace("E", "")
		val = val.replace("R", "")
		src_file = osp.join(src_dir, file_name)
		dst_file = osp.join(dst_dir, val + "_" + file_name)
		shutil.copy(src_file, dst_file)

def convert_path_to_gray(src_dir, dst_dir):
	mkdir(dst_dir)
	img_files = glob.glob(osp.join(src_dir, "*.jpg"))
	for f in img_files:
		dst_f = osp.join(dst_dir, osp.basename(f))
		Image.open(f).convert('L').save(dst_f)

def rename_bg_images(src_dir, dst_dir):
	mkdir(dst_dir)
	dirname = src_dir.split('/')[-1]
	image_files = glob.glob(os.path.join(src_dir, "*.png"))
	for i in range(len(image_files)):
		f = image_files[i]
		dst_file = osp.join(dst_dir, str(i)+'.jpg')
		shutil.copy(f, dst_file)




def recog_data_preprocess(srcpath, dstpath, flag = 0):

	if flag == 0:		
		random_count = 5
		with_quality = True
		file_ext = ".rec"

		dst_list_file = osp.join(dstpath, "recog_filelist.txt")				
		# extract_equation_crops(srcpath, dstpath, dst_list_file, file_ext, random_count=random_count, with_quality = with_quality)
		gen_data_list(dstpath)


	elif flag == 1:
		g_dst_type_list = ['1', '2']
		#srcpath = osp.join(g_base_dir, 'bankcard')
		#dstpath = osp.join(g_base_dir, 'results', "label_line_bankcard")
		#dstpath = osp.join(g_base_dir, 'results', "label_line_bankcard_lowJ")
		srcpath = osp.join(g_base_dir, 'car_plate')
		#dstpath = osp.join(g_base_dir, 'results', "label_line_car_plate")
		dstpath = osp.join(g_base_dir, 'results', "label_line_car_plate_lowJ")
		file_ext = ".box"
		dst_list_file = osp.join(dstpath, "data_list.txt")	
		with_quality = True
		extract_equation_crops(srcpath, dstpath, dst_list_file, file_ext, with_quality = with_quality)		
		#extract_equation_crops_det(srcpath, dstpath)
		#gen_data_list(dstpath)
	elif flag == 2:
		src_dir = osp.join(g_base_dir, 'labeled_phone')
		dst_dir = osp.join(g_base_dir, 'badcase_1')
		err_file = osp.join(g_base_dir, 'err_test.txt')
		extract_badcase(src_dir, dst_dir, err_file)
	elif flag == 3:
		src_dir = osp.join(g_base_dir, 'labeled_phone_gt')
		dst_dir = osp.join(g_base_dir, 'labeled_phone_gt_gray')
		convert_path_to_gray(src_dir, dst_dir)
	elif flag == 4:
		src_dir = '/data1/home/rexyuan/temp/jietu'
		dst_dir = '/data1/home/rexyuan/temp/jietu2'
		rename_bg_images(src_dir, dst_dir)
	elif flag == 5:
		#srcpath = osp.join(g_base_dir, "results", "label_line_bankcard")
		#is_driver = False
		
		#srcpath = osp.join(g_base_dir, "results", "driver")
		#is_driver = True
		
		#srcpath = osp.join(g_base_dir, "results", "label_line_car_plate")
		#is_driver = False

		#srcpath = osp.join(g_base_dir, "results", "label_line_bankcard_lowJ")
		#is_driver = False
		
		#srcpath = osp.join(g_base_dir, "results", "driver_lowJ")
		#is_driver = True
		
		srcpath = osp.join(g_base_dir, "results", "label_line_youtu20170808")
		is_driver = False

		dstpath = ""
		data_list = osp.join(srcpath, "data_list.txt")
		dst_data_list = osp.join(srcpath, "data_list_refine.txt")

		extract_valid_images(srcpath, dstpath, data_list, dst_data_list, is_driver)




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



