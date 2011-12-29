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
      
    file_list_url= 'http://www.kuaipan.cn/fileviewer/list/'
    
    download_info_url = r'http://www.kuaipan.cn/index.php?ac=fileview_handler&op=getdownurl&fileId=%s'
    
    download_url = r'%s/download/%s?etoken=%s&fileId=%s'
    
    sign_url = 'http://www.kuaipan.cn/index.php?ac=common&op=usersign'
    
    delete_url = 'http://www.kuaipan.cn/index.php?ac=fileview_handler&op=delete'
    
    rename_url = 'http://www.kuaipan.cn/index.php?ac=fileview_handler&op=rename'
    
    new_dir_url = 'http://www.kuaipan.cn/index.php?ac=fileview_handler&op=newdir'
    
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
            print '登陆成功'
            self.request_url(self.sign_url).read()
            print '签到成功！'
            return True
        else : return False
    
    def ls_file(self,kfile=None,recursion = False) :
        files = []       
        def parse_json(response) :
            if response :
                result = json.JSONDecoder().decode(response.read())
                if(result['result']['value'] == 'ok') :
                    for item in result['file'] :
                        if item : 
                            f = KFile.new_instance(**item)
                            print f
                            f.path = os.path.join(kfile and kfile.path or '' , f.name)
                            files.append(f)
                            if recursion and f.type == 'folder' : self.ls_file(f,recursion)
                    if kfile : kfile.list = files
                return files
        fileId = kfile and kfile.fileId or 'root'
        files = self.request_url(self.file_list_url,{'id':fileId},process = parse_json)
        return files
    
    def get_download_url(self,kfile):
        if kfile.type == 'file':
            download_info_url = self.download_info_url % (kfile.fileId)
            url_info = self.request_url(download_info_url,process = lambda content:
                                        json.JSONDecoder('utf-8').decode(content.read()[1:len(content.read())-1]))
            download_url = self.download_url % (url_info['url'],kfile.name,url_info['etoken'],kfile.fileId)
            return download_url
        else :
            return None
        
    def down_file(self,kfile,dest_dir,recursion = False):
        print 'sync file : %s ' % (kfile.path)
        if not os.path.exists(dest_dir) :
            os.makedirs(dest_dir)
        if kfile.type == 'file' :
            download_url = self.get_download_url(kfile)
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
    
    def new_dir(self,name,parent_file = None) :
        if parent_file and parent_file.type == 'file' :
            print '%s is not a dictionary !' % (parent_file.name)
            return False
        
        parentId = parent_file and parent_file.fileId or ''
        result = self.request_url(self.new_dir_url, {'parentid':parentId,'name':name},
                                  lambda response :json.JSONDecoder().decode(response.read()))
        
        if result and result['xLive_attr'] :
            if result['xLive_attr']['result'] in ('ok' , 'targetExist') :
                file = KFile.new_instance(**result['xLive'])
                file.path = os.path.join(parent_file and parent_file.path or '',name)
                return file
            else :
                return False
            
    def delete_file(self,kfile) :
        fileId = kfile and kfile.fileId
        if fileId:
            result = self.request_url(self.delete_url, {'fileid[]':fileId},
                             lambda response :json.JSONDecoder().decode(response.read()))
            print result
            if result and result[0]['result'] == 'ok' :
                return True
            else : return False
            
    def rename_file(self,kfile,new_name) :
        fileId = kfile and kfile.fileId
        if fileId and new_name:
            result = self.request_url(self.rename_url, {'fileid':fileId,'name':new_name},
                             lambda response :json.JSONDecoder().decode(response.read()))
            print result
            if result and result['result'] == 'ok' :
                return True
            else : return False
        
            
    def sync_all(self):
        pass
            
if __name__ == '__main__' :
    
    usrname = raw_input('username :')
    passwd = raw_input('password :')
    client = KuaiPan('/home/lei/kuaipan',usrname,passwd)
    client.login()
    kfile = client.new_dir('磊1')
    print kfile.fileId
    print client.rename_file(kfile, 'test')
    for f in client.ls_file() :
        print f.path
        
