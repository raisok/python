#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import json
from get_mut_result import MyThread
import sys
from time import ctime,sleep
import threading
import Queue
import time
import argparse


parser=argparse.ArgumentParser(description="This Program is used to get filename of case_id from TCGA \n.\
                            ",)
parser.add_argument('-id',action='store',help='set the id of case id you want to get.')
parser.add_argument('-output',action='store',help='set the output file name')
parser.add_argument('-version', action='version', version='%(prog)s 0.1')
args=parser.parse_args()


'''
Created on 2018年3月12日

@author: yueyao

利用多线程的方法写一个根据提交的id得到case_id的，再通过case_id找到对应的file_name的爬虫
可能会出现一个case_id对应多个file_name的情况

'''

#设置可以使用的最大线程数
threadmax = threading.BoundedSemaphore(20)

def read_file(file):
    # 读入输入文件并返回一个列表
    file_lis=[]
    with open (file,'r') as fr:
        for line in fr.readlines():
            line = line.strip()
            file_lis.append(line)
        return file_lis

def get_case_id(sub_id):
    case_id_dic={}
    get_case_id_url = 'https://api.gdc.cancer.gov/v0/graphql?hash=8212c05e2a46efabb53bcc37fddf49dc'
    get_case_id_post = {"id":"q3","query":"query RepositoryRoute {viewer {...F1}} fragment F0 on Case {case_id,project {project_id,id},submitter_id,id} fragment F1 on Root {_query11qEuO:query(query:\""+sub_id+"\",types:[\"case\"]) @include(if:true) {hits {id,__typename,...F0}}}","variables":{}}
    try:
        case_res = requests.post(get_case_id_url,data=json.dumps(get_case_id_post))
    except:
        print "I am getting case id, maybe has some ERROR!I will sleep 3 seconds and retry it"
        sleep(3)
        case_res = requests.post(get_case_id_url,data=json.dumps(get_case_id_post))
    result = case_res.text
    json_r = json.loads(result)
    lista = json_r['data']['viewer']['_query11qEuO']['hits']
    if len(lista) >=1:
        for i in range(len(lista)):
            case_id = json_r['data']['viewer']['_query11qEuO']['hits'][i]['case_id']
            submitter_id=json_r['data']['viewer']['_query11qEuO']['hits'][i]['submitter_id']
            project_id=json_r['data']['viewer']['_query11qEuO']['hits'][i]['project']['project_id']
            case_id_dic[case_id] = submitter_id
    return case_id_dic

def get_filename(case_id):
    get_filename_url='https://api.gdc.cancer.gov/v0/graphql/FilesTable?hash=0a224d9693627fe9795987c60976a46e'
    get_filename_post={"query":"query FilesTable_relayQuery(\n  $files_size: Int\n  $files_offset: Int\n  $files_sort: [Sort]\n  $filters: FiltersArgument\n) {\n  viewer {\n    repository {\n      files {\n        hits(first: $files_size, offset: $files_offset, sort: $files_sort, filters: $filters) {\n          total\n          edges {\n            node {\n              acl\n              id\n              file_name\n              file_size\n              access\n              file_state\n              state\n              file_id\n              data_category\n              data_format\n              platform\n              data_type\n              experimental_strategy\n              cases {\n                hits(first: 1) {\n                  total\n                  edges {\n                    node {\n                      case_id\n                      project {\n                        project_id\n                        id\n                      }\n                      id\n                    }\n                  }\n                }\n              }\n              annotations {\n                hits(first: 0) {\n                  total\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n","variables":{"files_size":20,"files_offset":0,"filters":{"op":"and","content":[{"op":"in","content":{"field":"cases.case_id","value":[case_id]}},{"op":"in","content":{"field":"files.analysis.workflow_type","value":["MuTect2"]}},{"op":"in","content":{"field":"files.data_category","value":["Simple Nucleotide Variation"]}},{"op":"in","content":{"field":"files.data_type","value":["Raw Simple Somatic Mutation"]}}]}}}
    try:
        file_name_re = requests.post(get_filename_url,data=json.dumps(get_filename_post))
    except:
        print "I'm getting file name,maybe has some ERROR!I will sleep 3 seconds and retry it"
        sleep(3)
        file_name_re = requests.post(get_filename_url,data=json.dumps(get_filename_post))
    result = file_name_re.text
    json_r = json.loads(result)
    lista = json_r['data']['viewer']['repository']['files']['hits']['edges']
    file_name_lis = []
    for i in range(len(lista)):
        file_name = lista[i]['node']['file_name']
        file_name_lis.append(file_name)
    return file_name_lis

def case_to_filename(q):
    while True:
        try:
            sub_id = q.get_nowait()
            i=q.qsize()
        except:
            print "Error!"
            break;
        final_lis=[]
        dic_case=get_case_id(sub_id)
        for i_key,i_value in dic_case.items():
            file_lis=get_filename(i_key)
            for j_file in file_lis:
                result=i_value+"\t"+i_key+"\t"+j_file
                final_lis.append(result)
        return final_lis

def queue_test(input_file,output_file):
    start=time.time()
    print "start time at:",ctime()
    q = Queue.Queue()
    fw=open(output_file,'w')
    file_lis = read_file(input_file)
    for sub_id in file_lis:
        q.put(sub_id)
    #先将文件读入列表
    # 可以开多个线程测试不同效果
    threads_lis=[]
    for i in range(10):
        t = MyThread(case_to_filename,args=(q,))
        threads_lis.append(t)
    for i in range(10):
        threads_lis[i].start()
    for i in range(10):
        threads_lis[i].join()
        for m in t.get_result():
            fw.write(m+"\n")
    fw.close()
    end=time.time()
    print "end time at:",ctime()
    print "ALL DONE %s" ,(end-start)
    

def get_result(sub_id):
    final_lis=[]
    dic_case=get_case_id(sub_id)
    for i_key,i_value in dic_case.items():
        file_lis=get_filename(i_key)
        for j_file in file_lis:
            result=i_value+"\t"+i_key+"\t"+j_file
            final_lis.append(result)
    threadmax.release()
    return final_lis

def multiple_run(input_file,output_file):
    start=time.time()
    print "start time at:",ctime()
    fw=open(output_file,'w')
    file_lis = read_file(input_file)
    threads=[]
    for sub_id in file_lis:
        threadmax.acquire()
        t = MyThread(get_result,args=(sub_id,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
        for m in t.get_result():
            fw.write(m+"\n")
    fw.close()
    end=time.time()
    print "end time at:",ctime()
    print "ALL DONE %s" ,(end-start)
 
         
if __name__ == '__main__':
    file_name=args.id
    output_file=args.ouput
    if args.id == None or args.output == None:
        print "Useage:\nMaybe you need to try python "+str(sys.argv[0])+" -h"
        sys.exit(0)
    multiple_run(file_name,output_file)
    #queue_test(file_name,output_file)
