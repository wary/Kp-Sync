#coding=utf-8
'''
Created on 2011-12-27

@author: lei
'''
import urllib2
import shutil
import os
import sys

def urllib2_down_load(url,dest) :
    try:
        print 'downing %s' % dest
        response = urllib2.urlopen(url)
        length = long(response.info().get('Content-Length'))
        if os.path.exists(dest) :
            print 'exists path %s' & (dest)
            return
        with open(dest,'wb') as output:
            data = response.read(1024)
            while data :
                output.write(data)
                data = response.read(1024)
                procetenge = output.tell()*100/length
                print '[%s%s] 完成 %d' %('>'*(20*procetenge/100),'-'*(20-procetenge*20/100),procetenge)
            print 'done'
    except Exception,e:
        print e 