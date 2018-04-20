#coding:utf-8
#将一种字符集产生的Text文件，转换为Label
import codecs
import argparse
import os
import sys

def read_tag_file(tag_file):
    file_io = codecs.open(tag_file,'r','utf-8')
    lines = file_io.readlines()
    file_io.close()
    tag_map = {}

    for line in lines:
        line = line.strip()  
        label,text = line.split()
        label = label.split(',')[0]
        tag_map[text] = label 
    return tag_map


parser = argparse.ArgumentParser() 
parser.add_argument(
    "text_file",
    help="input label file."
) 

parser.add_argument(
    "gtlabel_file",  
    help="label_file's tag map file"
) 

parser.add_argument(
    "output",  
    help="output label file"
)

args = parser.parse_args() 
text_file = args.text_file
tag_file = args.gtlabel_file 
output = args.output

# if os.path.exists(output):
#     print '%s is exists' % output
#     exit(-1)

tag_map = read_tag_file(tag_file)

file_io = codecs.open(text_file,'r','utf-8')
lines = file_io.readlines()
file_io.close() 

ignore_lines = []
file_io = open(output, 'w')

for line in lines:
    line = line.strip()  
    path, text = line.split() 
    tag_maps = ""
    for ch in text:
        if tag_map.has_key(ch):
            tag_maps = tag_maps + '%s,' %(tag_map[ch])
    file_io.write('%s %s\n' %(path, tag_maps[:len(tag_maps)-1]))

file_io.close()
if len(ignore_lines) > 0:
    print 'ignore labels:'
    for line in ignore_lines:
        print line



