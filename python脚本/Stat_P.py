#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import argparse
import logging


logging.getLogger().setLevel(logging.INFO)

""" 
@author:yueyao 
@file: Stat_P.py 
@time: 2018/06/22 
"""

def showhelp(moreinfo=""):
    help="""
        this program is to statistic the phos site . please use -h parameter to check detail
    """
    logging.info("%s%s",help,moreinfo)

def showneedinfo():
    needinfo="""
    数据格式说明：T表示苏氨酸，冒号后面的数值表示磷酸化的可能性；S表示丝氨酸，冒号后面的数值表示磷酸化的可能性；Y表示酪氨酸，冒号后面的数值表示磷酸化的可能性
要求：
1：对每行数据进行读取，只要有任何一个数据大于等于75的话把这行提取出来。
2：分别提取每行数值大于75的S（丝氨酸），T（苏氨酸），Y（酪氨酸）的个数，最后统计总的S，T，Y，的个数
3：如果这行只有一个大于75的数值，就算一个磷酸化位点
     如果这行只有二个大于75的数值，就算二个磷酸化位点
     如果这行只有三个大于75的数值，就算三个磷酸化位点
     如果这行只有三个以上大于75的数值，就算三个以上磷酸化位点
统计1，2，3，3个以上磷酸化位点的数目。

举例说明：数据前4列
T(5):	100	S(9):	100					一个T，一个S 属于两个磷酸化位点																						
S(6):	99.9	T(7):	0.2	S(8):	99.9			二个S 属于	两个磷酸化位点																				
S(3):	99.9	T(4):	0.2	S(6):	99.9	S(9):	0	两个S 属于两个磷酸化位点																					
T(3):	100	S(5):	0					一个T 属于1个磷酸化位点
								这四列都符合要求1
    """
    logging.info("%s",needinfo)

def read_file(locus,output,filter_num):
    total_t=0
    total_s=0
    total_y=0
    phos_site_1 =0
    phos_site_2 = 0
    phos_site_3 = 0
    phos_site_4 = 0

    fw =open(output,'w')
    with open (locus,'r') as f:
        for line in f.readlines():
            if line.startswith("Too"):
                continue
            count_t=0
            count_s=0
            count_y=0
            line = line.strip()
            lis = line.split('\t')
            for i in range(len(lis)):
                if lis[i].startswith("T"):
                    if float(lis[i+1]) >= filter_num:
                        count_t +=1
                elif lis[i].startswith("S"):
                    if float(lis[i+1]) >= filter_num:
                        count_s +=1

                elif lis[i].startswith("Y"):
                    if float(lis[i+1]) >= filter_num:
                        count_y +=1
                else:
                    pass
            line_total = count_t + count_s +count_y
            if line_total ==1:
                phos_site_1 +=1
            elif line_total == 2:
                phos_site_2 +=1
            elif line_total == 3:
                phos_site_3 +=1
            elif line_total >3:
                phos_site_4 +=1

            if count_y ==0 and count_s ==0 and count_t == 0:
                pass
            else:
                fw.write(line+"\tT_num:{t}\tS_num:{s}\tY_num:{y}\n".format(t=str(count_t),s=str(count_s),y=str(count_y)))
                # print (line+"\tT_num:{t}\tS_num:{s}\tY_num:{y}".format(t=str(count_t),s=str(count_s),y=str(count_y)))

            total_s +=count_s
            total_t +=count_t
            total_y +=count_y
        fw.write("one_phos_site:{one}\ttwo_phos_site:{two}\tthree_phos_site:{three}\tabove_three_phos_site:{above_th}\n".format(one=str(phos_site_1),two=str(phos_site_2),three=str(phos_site_3),above_th=str(phos_site_4)))
        fw.write("Total_S_Num:{to_s}\tTotal_T_Num:{to_t}\tTotal_Y_Num:{to_y}".format(to_s=str(total_s),to_t=str(total_t),to_y=str(total_y)))
        # print("one_phos_site:{one}\ttwo_phos_site:{two}\tthree_phos_site:{three}\tabove_three_phos_site:{above_th}".format(one=str(phos_site_1),two=str(phos_site_2),three=str(phos_site_3),above_th=str(phos_site_4)))
        # print ("Total_S_Num:{to_s}\tTotal_T_Num:{to_t}\tTotal_Y_Num:{to_y}".format(to_s=str(total_s),to_t=str(total_t),to_y=str(total_y)))
        fw.close()

if __name__ == "__main__":

    if len(sys.argv) == 1 :
        showhelp()
        showneedinfo()
        sys.exit()

    pwd = os.path.abspath('.')+"/result.xls"
    parser = argparse.ArgumentParser(description="statistic site num help")
    parser.add_argument('--output', dest='output', type=str, default=pwd,
                           help='the output file name you set ')
    parser.add_argument('--input', dest='input', type=str,
                            help="the file need to statistic.\n ")

    parser.add_argument('--threshold', dest='threshold', type=int, default=75,
                        help="the threshold you want to set.\n ")

    localeArg = parser.parse_args()

    read_file(localeArg.input,localeArg.output,localeArg.threshold)
