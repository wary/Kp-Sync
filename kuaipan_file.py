'''
Created on 2011-12-26

@author: lei
'''

class KFile:
    
    @staticmethod
    def new_instance( **kargs):
        kfile = KFile()
        if kargs :
            for k,v in kargs.items() :
                if hasattr(kfile, k) :
                    setattr(kfile, k, v or getattr(kfile, k))
        return kfile
                    
    def __init__(self) :
        self.name = None
        self.fileId = None
        self.type = None
        self.parentId = None
        self.sha1 = None
        self.size = None
        self.modTime = None
        self.createdTime = None
        self.shared = None
        self.fileVer = None
        self.opVer = None
        self.path = ''
        self.list = []
        
    def __str__(self):
        return  '%s : % s : %s : %s ' % (self.name,self.fileId,self.type,self.path)
    