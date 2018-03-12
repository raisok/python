#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Created on 2018年3月6日

@author: yueyao
'''

import sys
from bokeh.io import output_file
#这个写法是为了避免编码错误
reload(sys)
#sys.setdefaultencoding("utf-8")
import time
import requests
import json
import argparse


parser=argparse.ArgumentParser(description="This Program is used to get filename of case_id from TCGA \n.\
                            ",)
parser.add_argument('-id',action='store',help='set the id of case id you want to get.')
parser.add_argument('-output',action='store',help='set the output file name')
parser.add_argument('-version', action='version', version='%(prog)s 0.1')
args=parser.parse_args()



'''
从火狐复制post数据的时候直接可以当成字符串赋值给一个变量使用，如果需要修改post中的参数，需要定义一个变量，来改变post的参数
1.首先通过改变查询的id找到对应的case_id
2.通过case_id找到对应的filename
'''


def get_case_id(sub_id):
    case_id_dic={}
    #sub_id = "TCGA-A7-A0C"
    get_case_id_url = 'https://api.gdc.cancer.gov/v0/graphql?hash=8212c05e2a46efabb53bcc37fddf49dc'
    get_case_id_post = {"id":"q3","query":"query RepositoryRoute {viewer {...F1}} fragment F0 on Case {case_id,project {project_id,id},submitter_id,id} fragment F1 on Root {_query11qEuO:query(query:\""+sub_id+"\",types:[\"case\"]) @include(if:true) {hits {id,__typename,...F0}}}","variables":{}}
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
            print case_id + "\t"+ submitter_id+"\t"+ project_id    
    return case_id_dic
    
def get_filename(case_id):
    get_filename_url='https://api.gdc.cancer.gov/v0/graphql/FilesTable?hash=0a224d9693627fe9795987c60976a46e'
    get_filename_post={"query":"query FilesTable_relayQuery(\n  $files_size: Int\n  $files_offset: Int\n  $files_sort: [Sort]\n  $filters: FiltersArgument\n) {\n  viewer {\n    repository {\n      files {\n        hits(first: $files_size, offset: $files_offset, sort: $files_sort, filters: $filters) {\n          total\n          edges {\n            node {\n              acl\n              id\n              file_name\n              file_size\n              access\n              file_state\n              state\n              file_id\n              data_category\n              data_format\n              platform\n              data_type\n              experimental_strategy\n              cases {\n                hits(first: 1) {\n                  total\n                  edges {\n                    node {\n                      case_id\n                      project {\n                        project_id\n                        id\n                      }\n                      id\n                    }\n                  }\n                }\n              }\n              annotations {\n                hits(first: 0) {\n                  total\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n","variables":{"files_size":20,"files_offset":0,"filters":{"op":"and","content":[{"op":"in","content":{"field":"cases.case_id","value":[case_id]}},{"op":"in","content":{"field":"files.analysis.workflow_type","value":["MuTect2"]}},{"op":"in","content":{"field":"files.data_category","value":["Simple Nucleotide Variation"]}},{"op":"in","content":{"field":"files.data_type","value":["Raw Simple Somatic Mutation"]}}]}}}
    file_name_re = requests.post(get_filename_url,data=json.dumps(get_filename_post))
    result = file_name_re.text
    json_r = json.loads(result)
    lista = json_r['data']['viewer']['repository']['files']['hits']['edges']
    #num = json_r['data']['viewer']['repository']['files']['hits']['total']
    file_name_lis = []
    for i in range(len(lista)):
        file_name = lista[i]['node']['file_name']
        file_name_lis.append(file_name)
    return file_name_lis

def get_result(file_id,output_file):
    lis_id=[]
    with open (file_id,'r') as fr:
        for line in fr.readlines():
            line = line.strip()
            lis_id.append(line)
    with open (output_file+".download.txt",'w') as fw:
        for i in range(len(lis_id)):
            try:
                case_id_dic = get_case_id(lis_id[i])
            except Exception:
                print "Maybe some error happen ! I will Sleep 15 seconds"
                time.sleep(15)
                case_id_dic = get_case_id(lis_id[i])
            for case_id in case_id_dic.keys():
                try:
                    file_name_lis = get_filename(case_id)
                except Exception:
                    print "Maybe some error happen ! I will sleep 15 seconds"
                    time.sleep(15)
                    file_name_lis = get_filename(case_id)
                if file_name is None:
                    print "Maybe this case_id not exists!: " + case_id+"\t"+case_id_dic[case_id]
                else:
                    for j_file in file_name_lis:
                        fw.write(case_id_dic[case_id]+"\t"+ case_id+"\t"+j_file +"\n")
        
if __name__ == '__main__':
    
    file_name=args.id
    output_file=args.ouput
    if args.id == None or args.output == None:
        print "Useage:\nMaybe you need to try python "+str(sys.argv[0])+" -h"
        sys.exit(0)
    get_result(file_name,output_file)
