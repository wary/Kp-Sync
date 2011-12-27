#!/usr/bin/python
#coding=utf-8
'''
Created on 2011-12-25

@author: lei
'''
import os
import urllib
import urllib2
import cookielib
import json
import DownLoadUtil
import shutil
from BeautifulSoup import BeautifulSoup
from KFile import KFile

class KuaiPan :
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    
    get_fileview_url= lambda self,kfile : 'http://www.kuaipan.cn/index.php?ac=fileview&dirid=%s' % (kfile.fileid)
    
    get_download_info = lambda self,kfile : 'http://www.kuaipan.cn/index.php?ac=fileview_handler&op=getdownurl&fileId=%s' % (kfile.fileid)
    
    get_download_url = lambda self,kfile,url_info : \
                r'%s/download/%s?etoken=%s&fileId=%s' % (url_info['url'],kfile.name,url_info['etoken'],kfile.fileid)
    
    def __init__(self,username=None,passwd=None,cookiepath=r'.kuaipan.bat'):
        self.username=username
        self.passwd=passwd
        self.cookiepath=cookiepath
        self.cookiejar=cookielib.LWPCookieJar()
        if os.path.exists(self.cookiepath) :
            self.cookiejar.load(self.cookiepath)
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))

    
    def process_url(self,process,url,data=None,**args):
        try:
            if data :
                data = urllib.urlencode(data)
            request = urllib2.Request(url,data)
            request.headers = self.header
            page = self.opener.open(request)
            self.cookiejar.save(self.cookiepath,ignore_discard=True)
            return process(page.read(),**args)
        except IOError,e :
            print e
            return None
        
    def down_file(self,kfile,dest_dir):
        if not os.path.exists(dest_dir) :
            os.makedirs(dest_dir)
        if kfile.type == 'file' :
            download_info = self.get_download_info(kfile)
            decoder = json.JSONDecoder('utf-8')
            url_info = self.process_url(lambda content:decoder.decode(content[1:len(content)-1]),download_info)
            down_load_url = self.get_download_url(kfile,url_info)
            DownLoadUtil.urllib2_down_load(down_load_url, os.path.join(dest_dir,kfile.path))
            print '%s done!' % (kfile.name)
        elif kfile.type == 'folder' :
            self.dir_file(kfile)
            if not os.path.exists(os.path.join(dest_dir,kfile.path)) :
                os.makedirs(os.path.join(dest_dir,kfile.path))
            for f in kfile.list :
                print 'process path %s' % kfile.path 
                self.down_file(f,dest_dir)
    
    def sync_dir(self):
        pass
            
    def login(self) :
        url = r'http://www.kuaipan.cn/index.php?ac=account&op=login'
        data = urllib.urlencode({"username":self.username,"userpwd":self.passwd})
        request = urllib2.Request(url,data)
        self.opener.open(request)
        print 'login!'
        
    def get_fileList(self,webContent,**args) :
        files = []
        soup = BeautifulSoup(webContent)
        tags = soup('tbody',{'id':'filelistwrap'})
        if tags:
            if tags[0](id = 'nofilewrap') :
                return files
            filetags = tags[0]('tr')
            for tag in filetags :
                f = KFile()
                f.name = tag['filename']
                f.fileid = tag['fileid']
                f.type = tag["filetype"]
                if 'parentFile' in args :
                    f.path = os.path.join(args['parentFile'].path,f.name) 
                else :
                    f.path = os.path.join(f.path,f.name)
                files.append(f)
        return files
    
    def dir_file(self,kfile):
        if kfile.type != 'folder' :
            print kfile.type
            return []
        if not kfile.list:
            kfile.list = self.process_url(self.get_fileList, self.get_fileview_url(kfile),parentFile = kfile)
            
if __name__ == '__main__' :
    usrname = raw_input('username :')
    passwd = raw_input('password :')
    client = KuaiPan(usrname,passwd)
    client.login()
    page = client.opener.open('http://www.kuaipan.cn/index.php?ac=fileview')
    files = client.get_fileList(page.read())
    for f in files :
        client.down_file(f, '/home/lei/kuaipan')
    
    