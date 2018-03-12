#!/usr/bin/python
# -*- coding: UTF-8 -*-


'''
Created on 2018年3月12日

@author: yueyao

用于得到多线程调用函数返回的结果
'''

import threading


class MyThread(threading.Thread):
    '''
        用于获取多线的返回值
    '''
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args
    def run(self):
        self.result = self.func(*self.args)
    def get_result(self):
        try:
            return self.result # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None
