#coding:utf-8
__author__ = 'zhangxd18'
from ftplib import FTP
import time
import os
import shutil
import hashlib

def get_file_md5(filepath):
    # 获取文件的md5
    if not os.path.isfile(filepath):
        return
    myhash = hashlib.md5()
    f = open(filepath, "rb")
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    #print(myhash.hexdigest())
    return myhash.hexdigest()
    
def create_dir(local_path):
    if os.path.exists(local_path):
        pass
    else:
        cmd = 'mkdir ' + local_path
        #print cmd
        os.system(cmd)
            
def ftp_login(host,port,user,password):                          
    ftp = FTP()                                          
    try:
        ftp.connect(host,port)                           
    except:
        print "FTP connect failed!!!"
    try:
        ftp.login(user,password)                         
    except:
        print "FTP login failed!!!"                      
    else:
        return ftp                                       
        
def ftp_get_list(ftp,remote_path):
    ftp_dir_infos = []
    ftp.dir(remote_path, ftp_dir_infos.append)
    if remote_path[-1] == '\\':
        remote_path = remote_path[:-1]
    for dir_info in ftp_dir_infos:
        if dir_info.find('<DIR>') != -1:
            dir_info = remote_path+'\\'+dir_info.split()[-1]+'\\'
            ftp_get_list(ftp, dir_info)
        else:
            dir_info = remote_path+'\\'+dir_info.split()[-1]
        #print dir_info
        all_file_list.append(dir_info)
        
def ftp_download(ftp,remote_path,local_path):
    try:
        print remote_path, '===>', local_path
        local_dir=os.path.split(local_path)[0]
        #print local_dir
        create_dir(local_dir)
        
        bufsize = 1024
        local_file = open(local_path,'wb')               
        ftp.retrbinary('RETR %s'%(remote_path),local_file.write,bufsize)  
        ftp.set_debuglevel(0)
        local_file.close()                                         
    except Exception,e:
        print e
        print "download failed!!!\n"
    else:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        print "%s\ndownload succeed!!!\nMD5[%s]\n" %(current_time, get_file_md5(local_path))
            

if "__main__" == __name__:
    ftp = ftp_login('10.240.216.26', '21', 'anonymous', 'password')
    all_file_list = []
    remote_path = '.'
    local_path = 'Download'
    cur_py_file = os.path.realpath(__file__)
    local_path = os.path.split(cur_py_file)[0]+'\\'+local_path
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    ftp_get_list(ftp, remote_path)
    #print all_file_list
    for file in all_file_list:
        if file[-1] != '\\':
            ftp_download(ftp, file, local_path+'\\'+file[len(remote_path)+1:])
        else:
            create_dir(local_path+'\\'+file[len(remote_path)+1:])
    print '\n\n\n--------------The End--------------\n\n\n'
    
    
    
    
    
    
    
    
    