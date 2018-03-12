#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Authors: yueyao
# Data:2017-12-05

import sys
#这个写法是为了避免编码错误
reload(sys)
sys.setdefaultencoding("utf-8")
import requests
import json
import time
import argparse

parser=argparse.ArgumentParser(description="This Program is used to download TCGA Mutation Table\n.\
                            The default web url is \n:\
                            https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=1987780fc8671c1337a6c6682afd4e4d\n\
                            ",)
parser.add_argument('-id',action='store',help='set the id of cancer you want to download.')
parser.add_argument('-version', action='version', version='%(prog)s 0.1')
args=parser.parse_args()

def Cal_list(num,table_size):
    #根据表格的大小计算循环的次数
    count=num/table_size
    return count

def set_json_data(table_size,table_offset,tcga_name):
    #在这里设置表格展示的行数和每一行的起始编号，由于我们是从0开始计数，因此每次的开始都是整数
    #json的信息为向网址传输的参数，使用post的方法可以得到返回的信息，会储存在json格式的返回结果里，通过对json结果的解析得到想要的最终结果
    post_data={
        "query": "query SsmsTable_relayQuery(\n  $ssmTested: FiltersArgument\n  $ssmCaseFilter: FiltersArgument\n  $ssmsTable_size: Int\n  $consequenceFilters: FiltersArgument\n  $ssmsTable_offset: Int\n  $ssmsTable_filters: FiltersArgument\n  $score: String\n  $sort: [Sort]\n) {\n  viewer {\n    explore {\n      cases {\n        hits(first: 0, filters: $ssmTested) {\n          total\n        }\n      }\n      filteredCases: cases {\n        hits(first: 0, filters: $ssmCaseFilter) {\n          total\n        }\n      }\n      ssms {\n        hits(first: $ssmsTable_size, offset: $ssmsTable_offset, filters: $ssmsTable_filters, score: $score, sort: $sort) {\n          total\n          edges {\n            node {\n              id\n              score\n              genomic_dna_change\n              mutation_subtype\n              ssm_id\n              consequence {\n                hits(first: 1, filters: $consequenceFilters) {\n                  edges {\n                    node {\n                      transcript {\n                        is_canonical\n                        annotation {\n                          impact\n                        }\n                        consequence_type\n                        gene {\n                          gene_id\n                          symbol\n                        }\n                        aa_change\n                      }\n                      id\n                    }\n                  }\n                }\n              }\n              filteredOccurences: occurrence {\n                hits(first: 0, filters: $ssmCaseFilter) {\n                  total\n                }\n              }\n              occurrence {\n                hits(first: 0, filters: $ssmTested) {\n                  total\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n",
        "variables": {
            "ssmTested": {
                "op": "and",
                "content": [
                    {
                        "op": "in",
                        "content": {
                            "field": "cases.available_variation_data",
                            "value": [
                                "ssm"
                            ]
                        }
                    }
                ]
            },
            "ssmCaseFilter": {
                "op": "and",
                "content": [
                    {
                        "op": "in",
                        "content": {
                            "field": "available_variation_data",
                            "value": [
                                "ssm"
                            ]
                        }
                    },
                    {
                        "op": "in",
                        "content": {
                            "field": "cases.project.project_id",
                            "value": [
                                tcga_name
                            ]
                        }
                    }
                ]
            },
            "ssmsTable_size": table_size,   #这一个用来控制表格的大小，这里尝试用设置一个很大的值然后将所有的信息全部下载下来
            "consequenceFilters": {
                "op": "NOT",
                "content": {
                    "field": "consequence.transcript.annotation.impact",
                    "value": "missing"
                }
            },
            "ssmsTable_offset": table_offset,  #用来控制列表的起始位置
            "ssmsTable_filters": {
                "op": "and",
                "content": [
                    {
                        "op": "in",
                        "content": {
                            "field": "cases.project.project_id",
                            "value": [
                                tcga_name
                            ]
                        }
                    }
                ]
            },
            "score": "occurrence.case.project.project_id",
            "sort": [
                {
                    "field": "_score",
                    "order": "desc"
                },
                {
                    "field": "_uid",
                    "order": "asc"
                }
            ]
        }
    }
    return post_data

def set_url(tcga_name):
    dict_url={
        'TCGA-GBM':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=a2872044bb80fef077654e5e9a30ca8a',
        'TCGA-KIRC':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=b2d7cd5b6275385da74a6bd37c437139',
        'TCGA-KIRP':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=fa80a8e7e133b1903d5abf42477cfb65',
        'TCGA-KICH':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=0d0f9b8d73760acb1845a0ea63b17e9f',
        'TCGA-BLCA':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=4482bacb61cf377d99437a3d8b186c69',
        'TCGA-LGG':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=b3d410f1ea38c691193f8126c7be1a0f',
        'TCGA-BRCA':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=ac612ca7ba974561ac0b0fb4ccb5379e',
        'TCGA-COAD':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=3f7aa2c63d8c1c51e0697c578239344c',
        'TCGA-READ':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=6264a4380d3e8a5edcc63f4e826319de',
        'TCGA-LUAD':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=e00056998ffa1a3f9ecbee61f27acc00',
        'TCGA-LUSC':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=928ea5fcf73f5ec60a41671da17d6ece',
        'TCGA-OV':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=0b2b69e8129649fb5637fb2bd920f8c1',
        'TCGA-SKCM':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=c9b2ad1c42cbe72f0a86937e85373edd',
        'TCGA-STAD':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=036fca5ae7b2f0c73146c1180d711c69',
        'TCGA-UCEC':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=af415a152494bdbacec1152a29bb10c5',
        'TCGA-UCS':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=af415a152494bdbacec1152a29bb10c5',
        'TCGA-PRAD':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=0a80d38186154aff1bd0bbe810451fd7',
        'TCGA-THCA':'https://api.gdc.cancer.gov/v0/graphql/SsmsTable?hash=0a80d38186154aff1bd0bbe810451fd7'
    }
    return dict_url[tcga_name]

def print_title():
    title="Mutation ID\tDNA Change\tType\tConsequences\t# Affected Cases in Cohort\t# Affected Cases Across the GDC    Impact (VEP)"
    return title
    
def write_result(tcga_name,num):
    title=print_title()
    fh=open(tcga_name+'.txt','a')
    fh.write(title+'\n')
    num=int(num)
    table_size=500
    count = Cal_list(num,table_size)
    url = set_url(tcga_name)
    i_key=0
    while (i_key <= count):
    #for i_key in range(0,count+1):
        table_offset=i_key*table_size
        post_json=set_json_data(table_size,table_offset,tcga_name)
        try:
            req = requests.post(url,data=json.dumps(post_json))
        except Exception:
            j=1
            print "I got a error,I will retry after 30s for three times"
            while j<=3:
                time.sleep(30)
                try:
                    req = requests.post(url,data=json.dumps(post_json))
                    break
                except Exception:
                    j+=1
                    if j==3:
                        print "I don't know how to deal with it,the program is over here,please check it carefully"
                        os.system('touch Interrupt_at_round_'+i+'.errorlog')
                        sys.exit(0)
                    else:
                        print "Retry times:"+str(j)
                else:
                    print "The problem maybe solve here"
        else:
            print "I work it normally on "+str(i_key)+" round"
		try:
			result = req.text
			json_r = json.loads(result)
		except KeyError:
			i_key = i_key -1
			next
		else:
			print "JSON Load OK!"
        try:
            for i in range(table_size):
                filter_cases=json_r['data']['viewer']['explore']['filteredCases']['hits']['total']
                cases=json_r['data']['viewer']['explore']['cases']['hits']['total']
                dna_change=json_r['data']['viewer']['explore']['ssms']['hits']['edges'][i]['node']['genomic_dna_change']
                m_type=json_r['data']['viewer']['explore']['ssms']['hits']['edges'][i]['node']['mutation_subtype']
                occurrence=json_r['data']['viewer']['explore']['ssms']['hits']['edges'][i]['node']['occurrence']['hits']['total']
                score=json_r['data']['viewer']['explore']['ssms']['hits']['edges'][i]['node']['score']
                ssm_id=json_r['data']['viewer']['explore']['ssms']['hits']['edges'][i]['node']['ssm_id']
                total_num=json_r['data']['viewer']['explore']['ssms']['hits']['total']
                Across_the_GDC=str(occurrence)+'/'+str(cases)
                in_Cohort=str(score)+'/'+str(filter_cases)
                in_Cohort_rate=float(score)/float(filter_cases)*100.00
                float_in_Cohort_rate=str(float('%.2f' % in_Cohort_rate))+'%'
                impact=json_r['data']['viewer']['explore']['ssms']['hits']['edges'][i]['node']['consequence']['hits']['edges'][0]['node']['transcript']['annotation']['impact']
                consequence_type=json_r['data']['viewer']['explore']['ssms']['hits']['edges'][i]['node']['consequence']['hits']['edges'][0]['node']['transcript']['consequence_type']
                gene_symbol=json_r['data']['viewer']['explore']['ssms']['hits']['edges'][i]['node']['consequence']['hits']['edges'][0]['node']['transcript']['gene']['symbol']
                aa_change=json_r['data']['viewer']['explore']['ssms']['hits']['edges'][i]['node']['consequence']['hits']['edges'][0]['node']['transcript']['aa_change']
                #判断是否aa_change为null,m_type和consequence_type的值使用原始值
                fh.write( str(ssm_id)+'\t'+str(dna_change)+'\t'+str(m_type)+'\t'+str(consequence_type)+' '+str(gene_symbol)+' '+str(aa_change)+'\t'+str(in_Cohort)+','+str(float_in_Cohort_rate)+'\t'+str(Across_the_GDC)+'\t'+str(impact)+'\t'+'\n')
        except IndexError:
            print "If it has a error about index, it means the table is over"
            os.system('touch '+tcga_name+'.ok.txt')
        except KeyError:
            i_key = i_key-1
            print "I will redownload it at " +str(i_key) +" cycle"
            os.system('touch '+tcga_name+'_'+str(i_key)+'.marker.txt')
            next
        else:
            print "Sussessful write the file\t"+str(tcga_name)+'.txt\t'+str(table_offset)
        i_key +=1
    fh.close()

def TCGA_DATA():
    dict_tcga={
        'TCGA-KIRP':25723,
        'TCGA-KICH':3248,
        'TCGA-BLCA':144180,
        'TCGA-GBM':89826,
        'TCGA-LGG':38417,
        'TCGA-BRCA':128359,
        'TCGA-COAD':274779,
        'TCGA-READ':70999,
        'TCGA-LUAD':222411,
        'TCGA-LUSC':194316,
        'TCGA-OV':79849,
        'TCGA-SKCM':395572,
        'TCGA-STAD':215136,
        'TCGA-UCEC':920527,
        'TCGA-UCS':10938,
        'TCGA-PRAD':31332,
        'TCGA-THCA':11029,
        'TCGA-KIRC':28761
    }
    return dict_tcga

if __name__ == '__main__':
    tcga_name=args.id
    if args.id == None:
        print "Useage:\nMaybe you need to try python "+str(sys.argv[0])+" -h"
        sys.exit(0)
    data=TCGA_DATA()
    gene_num = str(data[tcga_name])
    write_result(tcga_name,gene_num)
