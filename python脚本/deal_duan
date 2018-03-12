#!/usr/bin/python
'''
This script is used for count the modify site.The input file type are as follow.
You need to statistics the values above 90 in each line and print the result.
########################################
phosphoRS Site Probabilities
S(2): 93.3; S(5): 11.1; S(6): 63.9; S(7): 65.9; S(8): 65.9; S(15): 0.0
T(10): 99.9; S(11): 80.0; S(12): 80.0; S(13): 80.0; S(14): 80.0; S(15): 80.0
T(10): 100.0; S(11): 100.0; S(12): 100.0; S(13): 100.0; S(14): 100.0; S(15): 100.0
S(1): 0.0; T(4): 0.0; S(18): 100.0; S(20): 100.0
Too many isoforms
T(4): 0.0; S(9): 100.0; T(11): 100.0
S(4): 100.0; T(6): 100.0
#########################################
'''
import re
import sys
import string
import math
count0,count1,count2,count3,count4,count5=[0,0,0,0,0,0]
list0,list1,list2,list3,list4=[],[],[],[],[]
dic={}
dic[count1] = '1'
dic[count0] = '0'
dic[count2] = '2'
dic[count3] = '3'
dic[count4] = '4'
with open(sys.argv[1],'r') as fr:
	fr.readline()
	for line in fr.readlines():
		if (re.match(r'Too',line)):
			continue
		else:
			line = line.strip()
			listtemp =[]
			listtemp = line.split(';')
			temp=[]
			countnumber=0
			for modify in listtemp:
				modify = modify.strip()
				temp = modify.split(': ')
				tempf = float(temp[-1])
				if (tempf >= 90.0):
					countnumber+=1
		if(countnumber ==1):
			count1+=1
			list1.append(line)
		elif(countnumber ==2):
			count2+=1
			list2.append(line)
		elif(countnumber ==3):
			count3+=1
			list3.append(line)
		elif(countnumber >=4):
			count4+=1
			list4.append(line)
		else:
			count0+=1
			list0.append(line)
def seqcount(num,lista):
	with open(sys.argv[2],'a') as fd:
		fd.write("The seq contain " + dic[num] +" modify site is :" + str(num) +"\n")
		for la in lista:
			fd.write(la+'\n')
if __name__ == '__main__':
	seqcount(count0,list0)
	seqcount(count1,list1)
	seqcount(count2,list2)
	seqcount(count3,list3)
	seqcount(count4,list4)
