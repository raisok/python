#!/usr/bin/python
# -*- coding: utf-8 -*-

#这个脚本用于批量修改碱基质量图和热图的名字；

import re
import sys
import os;
dic={}
with open (sys.argv[1],'r' )as file:
    for line in file.readlines():
        line = line.strip()
        lis = line.split('\t')
        namekey = lis[2]
        namebase = namekey + ".base"
        namequal = namekey + ".qual"
        namevalue = lis[0]
        namevaluebase = namevalue + ".base"
        namevaluequal = namevalue + ".qual"
        dic[namebase] = namevaluebase
        dic[namequal] = namevaluequal
#for i_key in dic.keys():
#    print (i_key+"\t"+dic[i_key])
def rename():
    path="E:\\橡胶项目\\转录组结果\\91result\\rename_base_pic";
    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
    for files in filelist:#遍历所有文件
        Olddir=os.path.join(path,files);#原来的文件路径
        if os.path.isdir(Olddir):#如果是文件夹则跳过
            continue;
        filename=os.path.splitext(files)[0];#文件名
        filetype=os.path.splitext(files)[1];#文件扩展名
        Newdir=os.path.join(path,dic[filename]+filetype);#新的文件路径
        os.rename(Olddir,Newdir);#重命名
rename()
