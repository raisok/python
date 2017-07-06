#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import os
import sys
import time
import argparse

def opt():
	#实例化一个OptionParser对象
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', action='store', dest='file_name',
						help='file you want to check')
		
	parser.add_argument("-c","--check",dest="check",action="store_false",default=True,
						help="set yes/no to decide run program or not,defalut=yes"	)
	#调用parse_args解析参数，返回(option,args)元组
	results = parser.parse_args()
	return results


def Check_file(file):
	flag = 0
	while flag < 10:
		if os.path.isfile(file):
			print "the file a exists!"
			sys.exit()
		else:
			print "the file doesn't exist, Please check it carefully!"
			time.sleep(2)
			flag = flag +1

if __name__ == '__main__':
	option=opt()
	if option.check :
		Check_file(option.file_name)
	else:
		print "you set parameter no, do not check the file !"