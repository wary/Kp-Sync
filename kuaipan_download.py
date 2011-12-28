#coding=utf-8
'''
Created on 2011-12-27

@author: lei
'''
import urllib2
import shutil
import os

def urllib2_down_load(url,dest) :
    try:
        print 'downing %s' % dest
        response = urllib2.urlopen(url)
        import shutil
        if os.path.exists(dest) :
            print 'exists path %s' & (dest)
            return
        
        with open(dest,'wb') as output:
            shutil.copyfileobj(response, output)
        print dest
    except Exception,e:
        print e 