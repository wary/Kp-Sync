'''
Created on 2011-12-26

@author: lei
'''
class KFile:
    def __init__(self) :
        self.name = None
        self.fileid = None
        self.type = None
        self.path = ''
        self.list = []
        
    def __str__(self):
        return  '%s : % s : %s : %s ' % (self.name,self.fileid,self.type,self.path)