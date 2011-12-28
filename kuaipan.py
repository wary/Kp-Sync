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
from kuaipan_download import urllib2_down_load
from BeautifulSoup import BeautifulSoup
from kuaipan_file import KFile

class KuaiPan :
    
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    
    login_url = r'http://www.kuaipan.cn/index.php?ac=account&op=login'
    
    root_url = r'http://www.kuaipan.cn/index.php?ac=fileview'
    
    fileview_url= r'http://www.kuaipan.cn/index.php?ac=fileview&dirid=%s'
    
    download_info_url = r'http://www.kuaipan.cn/index.php?ac=fileview_handler&op=getdownurl&fileId=%s'
    
    download_url = r'%s/download/%s?etoken=%s&fileId=%s'
    
    sign_url = 'http://www.kuaipan.cn/index.php?ac=common&op=usersign'
    
    delete_url = 'http://www.kuaipan.cn/index.php?ac=fileview_handler&op=delete'
    
    def __init__(self,root,username,passwd,cookiepath=r'.kuaipan.bat'):
        self.root = root
        self.username=username
        self.passwd=passwd
        self.cookiepath=cookiepath
        self.cookiejar=cookielib.LWPCookieJar()
        if os.path.exists(self.cookiepath) :
            self.cookiejar.load(self.cookiepath)
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
        
    def request_url(self,url, data = None, process = None,*args, **kargs):
        try:
            if data :
                data = urllib.urlencode(data)
            request = urllib2.Request(url,data,headers = self.header)
            response = self.opener.open(request)
            self.cookiejar.save(self.cookiepath,ignore_discard=True)
            if process :
                if args :
                    return process(response,*args,**kargs)
                else :
                    return process(response)
            else :
                return response
        except IOError,e :
            print e
            return None
        
    def login(self) :
        data = {"username":self.username,"userpwd":self.passwd}
        response = self.request_url( self.login_url, data)
        if not response.read().find('签到') == -1 :
            print self.request_url(self.sign_url).read()
            return True
        else : return False
    
    def ls_file(self,kfile,recursion = False) :
        def parse_page(response) :
            files = []
            if response :
                soup = BeautifulSoup(response.read())
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
                        f.path = os.path.join(kfile.path,f.name)
                        f.server_time = tag('td',{'class':'tr'})[0].text
                        if recursion :
                            self.ls_file(f, recursion)
                        files.append(f)
            kfile.list = files
            return files
        
        if kfile :
            if kfile.type == 'file' :
                return []
            else :
                if kfile.type == 'root' :
                    ls_url = self.root_url
                else :
                    ls_url = self.fileview_url % (kfile.fileid)
                files = self.request_url(ls_url,process = parse_page)
        return files
    
    def get_download_url(self,kfike):
        if kfile.type == 'file':
            download_info_url = self.download_info_url % (kfile.fileid)
            url_info = self.request_url(download_info_url,process = lambda content:
                                        json.JSONDecoder('utf-8').decode(content.read()[1:len(content.read())-1]))
            download_url = self.download_url % (url_info['url'],kfile.name,url_info['etoken'],kfile.fileid)
        else :
            return None
        
    def down_file(self,kfile,dest_dir,recursion = False):
        print 'sync file : %s ' % (kfile.path)
        if not os.path.exists(dest_dir) :
            os.makedirs(dest_dir)
        if kfile.type == 'file' :
            download_url = self.get_download_url(kfike)
            if download_url :
                urllib2_down_load(download_url, os.path.join(dest_dir,kfile.path))
            print '%s done!' % (kfile.name)
        elif kfile.type == 'folder' :
            self.ls_file(kfile)
            if not os.path.exists(os.path.join(dest_dir,kfile.path)) :
                os.makedirs(os.path.join(dest_dir,kfile.path))
            if recursion :
                for f in kfile.list :
                    print 'process path %s' % kfile.path 
                    self.down_file(f,dest_dir,recursion)
                
    def sync_all(self):
        pass
            
if __name__ == '__main__' :
    usrname = raw_input('username :')
    passwd = raw_input('password :')
    client = KuaiPan('/home/lei/kuaipan',usrname,passwd)
    client.login()
    root = KFile()
    root.type = 'root'
    files = client.ls_file(root,recursion=True)
    for f in files :
        print f
        #client.down_file(f,'/home/lei/kuaipan',True)
        
