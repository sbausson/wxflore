#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import re
import unicodedata

current_path = os.getcwd()
fnroot = current_path.split("/")[-1]

i = 1

# os.listdir(".")
for filename in os.listdir(u'.'): #[unicodedata.normalize('NFC', f) for f in os.listdir(u'.')]:

    src = filename #filename.decode('utf8') #,errors='ignore')

    if not re.match("{}.[0-9][0-9].jpg".format(fnroot),filename):
        dst = u"{}.{:02d}.jpg".format(fnroot,i)

        while os.path.exists(dst):
            i+=1
            dst = "{}.{:02d}.jpg".format(fnroot,i)

        if os.path.exists(dst):
            print("## WARNING ## : Ignoring  {} --> {} (File alread exists)".format(src,dst))
        elif not re.match("[A-Z]",fnroot):
            print("## WARNING ## : Ignoring  {} --> {} (Bad DIR name)".format(src,dst))
        elif os.path.isdir(src):
            print("## WARNING ## : Ignoring  {} --> {} (Do not rename DIR's)".format(src,dst))
        else:
            #print(type(src))
            #print(type(dst))

            if isinstance(src,unicode):
                s=u"Renaming {} --> {}".format(src,dst)
                print(s) #.encode('utf8','surrogateescape'))
            elif isinstance(src,str):
                s=u"Renaming {} --> {}".format(src.decode('utf8',errors='ignore'),dst)
                print(s.encode('utf8','surrogateescape'))
            else:
                error()

            os.rename(src,dst)

        i+=1
