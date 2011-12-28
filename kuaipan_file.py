'''
Created on 2011-12-26

@author: lei
'''
import inspect

class KFile:
    def __init__(self) :
        self.name = None
        self.fileid = None
        self.type = None
        self.path = ''
        self.server_time = None
        self.local_time = None
        self.list = []
    
    def __str__(self):
        return  '%s : % s : %s : %s ' % (self.name,self.fileid,self.type,self.path)