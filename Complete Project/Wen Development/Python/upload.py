#!/usr/bin/python3

import requests as req
import os.path, os
import ftplib 
from ftplib import FTP, error_perm

ftp = ftplib.FTP('roadquality.ca')
ftp.login("natnael@roadquality.ca","natnael")
ftp.cwd('public_html/data')
filenameCV = "/home/pi/Documents/capstone2018/Talha/upload_real_time/Wascana_Pkways"
def placeFiles(ftp, path):
    for name in os.listdir(path):
        localpath = os.path.join(path, name)
        if os.path.isfile(localpath):
            print("STOR", name, localpath)
            ftp.storbinary('STOR ' + name, open(localpath,'rb'))
        elif os.path.isdir(localpath):
            print("MKD", name)

            try:
                ftp.mkd(name)

            # ignore "directory already exists"
            except error_perm as e:
                if not e.args[0].startswith('550'): 
                    raise

            print("CWD", name)
            ftp.cwd(name)
            placeFiles(ftp, localpath)           
            print("CWD", "..")
            ftp.cwd("..")

placeFiles(ftp, filenameCV)

""" filename = "sending.csv"
ftp = ftplib.FTP('roadquality.ca')
ftp.login("natnael@roadquality.ca","natnael")
ftp.cwd('public_html/data')
myfile = open('/Users/User/Desktop/sending.csv','rb')
ftp.storlines('STOR '+filename, myfile) """


resp = req.get("http://roadquality.ca/upload.php")
print(resp.text)
