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
        text  = text.split(',')[0]

        tag_map[label] = text
        # tag_map[label] = text.encode("ascii","ignore")
    return tag_map

    # for line in lines:
    #     line = line.strip()  
    #     label,text = line.split()
    #     label = label.split(',')[0]
    #     tag_map[text] = label 
    # return tag_map



parser = argparse.ArgumentParser() 
parser.add_argument(
    "label_file",
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
label_file = args.label_file
tag_file = args.gtlabel_file 
output = args.output

# if os.path.exists(output):
#     print '%s is exists' % output
#     exit(-1)

tag_map = read_tag_file(tag_file)

file_io = codecs.open(label_file,'r','utf-8')
lines = file_io.readlines()
file_io.close() 

ignore_lines = []
file_io = codecs.open(output, 'w','utf-8')

print tag_map

for line in lines:
    line = line.strip()  
    path, text = line.split() 

    print text
    tag_maps = ""
    for ch in text.split(','):
        if tag_map.has_key(ch):
            # print ch,tag_map[ch]
            tag_maps = tag_maps + '%s' %(tag_map[ch])

    # tag_maps = tag_maps.encode('utf-8')
    file_io.write('%s %s\n' %(path, tag_maps))



file_io.close()
if len(ignore_lines) > 0:
    print 'ignore labels:'
    for line in ignore_lines:
        print line



