#!/usr/bin/env python


#encoding:utf-8
'''
Created on 2017.5.29

@author: zhura
'''

class GOBase(object):
    def __init__(self,_id):
        self._id=_id
        self.alt_ids=[]
        self.name=''
        self.namespace=''
        self.parent=None
        self.level=-1 
        self.allParents=None 
        
class ObOs(object):
    def __init__(self,path):
        self.path=path
        self.map={}
        self.parseObO()
    def parseObO(self):
        f=open(self.path)
        lines=f.readlines()
        f.close()
        _goTxt=[]
        flag=False
        for line in lines:
            line=line.rstrip('\n').strip()
            if flag:
                _goTxt.append(line)
            if flag and line=='':
                self.parseGO(_goTxt)
                _goTxt=[]
                flag=False
            if line.find('[Term]')==0:
                flag=True
                
    def parseGO(self,_goText):
        _id=None
        _name=''
        _namespace=''
        _is_as=[]
        _alt_ids=[]
        for _txt in _goText:
            if _txt.find('id:')==0:
                _id=_txt[_txt.find('GO'):_txt.find('GO')+10]
            elif _txt.find('name:')==0:
                _name=_txt[5:len(_txt)].rstrip().lstrip()
            elif _txt.find('namespace:')==0:
                _namespace=_txt[10:len(_txt)].rstrip().lstrip()
            elif _txt.find('alt_id:')==0:
                _alt_ids.append(_txt[_txt.find('GO'):_txt.find('GO')+10]) 
            elif _txt.find('is_a:')==0 or _txt.find('relationship:')==0:
                _is_as.append(_txt[_txt.find('GO'):_txt.find('GO')+10]) 
        if _id:
            _go=None
            if self.map.has_key(_id):
                _go=self.map[_id]
            else:
                _go=GOBase(_id)   
            _go.name=_name
            _go.namespace=_namespace   
            _go.parent=self.parseParent(_is_as)
            _go.alt_ids=_alt_ids
            self.map[_id]=_go
            if len(_alt_ids)>0:
                for _alt in _alt_ids:
                    self.map[_alt]=_go 
                               
    def parseParent(self,is_as):
        __parent=[]
        for isa in is_as:
            if not self.map.has_key(isa):
                cGo=GOBase(isa)
                self.map[isa]=cGo
            __parent.append(isa)
        return __parent
    
    def getLevel(self,_id):
        _min=100000
        _go=self.map[_id]
        if _go.level>0:
            pass
        elif len(_go.parent)==0:
            _go.level=1
        else:
            for g in _go.parent:
                lev=self.getLevel(g)
                if _min>lev:
                    _min=lev
            _go.level=_min+1
        return _go.level
    
    def getAllParent(self,_id):
        _prs=[_id]
        _go=self.map[_id]
        if not _go.allParents is None:
            return _go.allParents
        if _go.parent is None or len(_go.parent)==0:
            _go.allParents=_prs
            return _go.allParents
        for g in _go.parent:
            ap=self.getAllParent(g)
            _prs.extend(ap)
        _go.allParents=list(set(_prs))
        return _go.allParents  

if __name__ == '__main__':
    obo='D:/bgDB/go-basic.obo.txt'
    ob=ObOs(obo)
    print ob.getAllParent('GO:0004322')
    print ob.getLevel('GO:0004322')
    print ob.getLevel('GO:0003824')