#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import re
import click


""" 
@author:yueyao 
@file: Get_Promote.py 
@time: 2018/07/18 
"""


def regex():
    pattern=re.compile(r'[AT]GATA[AG]')
    return pattern

def read_pos(file):
    dic_chr_gene={}
    with open(file,'r') as file:
        for line in file.readlines()[1:]:
            line =line.strip()
            geneid=line.split('\t')[0]
            pos=line.split('\t')[1]
            chrname=pos.split(':')[0]
            gene_start=pos.split(':')[1].split('-')[0]
            promote_pos_start = int(gene_start)-1000
            if chrname in dic_chr_gene.keys():
                dic_chr_gene[chrname].append([geneid,gene_start,promote_pos_start])
            else:
                dic_chr_gene[chrname]=[]
                dic_chr_gene[chrname].append([geneid, gene_start, promote_pos_start])
    return dic_chr_gene

def read_go(annot):
    dic_go={}
    with open(annot,'r') as gofile:
        for line in gofile.readlines():
            line = line.strip()
            arr = re.split('[\s\t]',line)
            geneid=arr[0]
            goid=arr[1]
            if geneid in dic_go.keys():
                dic_go[geneid].append(goid)
            else:
                dic_go[geneid]=[]
                dic_go[geneid].append(goid)
    return dic_go

@click.command()
@click.argument('genome')
@click.argument('file')
@click.argument('annot')
def read_genome(genome,file,annot):
    seq_list=[]
    dic_genome={}
    dic_gene_pro={}
    pattern=regex()
    dic_go = read_go(annot)
    pro_seq=open('pro_seq.fa','w')
    all_seq=open('all_seq.fa','w')
    pro_gene_go=open('pro_gene_go.annot','w')
    with open (genome,'r') as genome:
        for line in genome.readlines():
            line = line.strip()
            if line.startswith('>'):
                id=line.lstrip('>')
                seq_list=[]
            else:
                seq_list.append(line)
                dic_genome[id]=seq_list
    dic_chr_gene = read_pos(file)
    for chr_i,pos_lis in dic_chr_gene.items():
        if len(pos_lis) >1:
            for m in pos_lis:
                tempseq = "".join(dic_genome[chr_i])
                geneseq = tempseq[int(m[2])-1:int(m[1])-1]
                dic_gene_pro[m[0]]=geneseq
                re_s=re.search(pattern,geneseq)
                all_seq.write(">"+m[0]+"\n")
                all_seq.write(geneseq+"\n")
                if re_s:
                    pro_seq.write(">"+m[0]+"\n")
                    pro_seq.write(geneseq + "\n")
                    if m[0] in dic_go.keys():
                        pro_gene_go.write(m[0]+"\t"+"\t".join(dic_go[m[0]])+"\n")
                    else:
                        print(m[0] + "\tnot has go annotation")
        else:
            tempseq ="".join(dic_genome[chr_i])
            geneseq = tempseq[int(m[2]) - 1:int(m[2]) - 1 + 1000]
            dic_gene_pro[m[0]] = geneseq
            re_s = re.search(pattern, geneseq)
            all_seq.write(">" + m[0] + "\n")
            all_seq.write(geneseq + "\n")
            if re_s:
                pro_seq.write(">" + m[0] + "\n")
                pro_seq.write(geneseq + "\n")
                if m[0] in dic_go.keys():
                    pro_gene_go.write(m[0] + "\t" + ",".join(dic_go[m[0]]) + "\n")
                else:
                    print(m[0]+"\tnot has go annotation")

    pro_seq.close()
    all_seq.close()
    pro_gene_go.close()

if __name__ == '__main__':
    read_genome()
