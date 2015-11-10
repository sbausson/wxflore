#!/usr/bin/env python3

import os
import re

current_path = os.getcwd()
fnroot = current_path.split("/")[-1]

i = 1
for filename in os.listdir("."):

    src = filename
    if not re.match("{}.[0-9][0-9].jpg".format(fnroot),filename):
        dst = "{}.{:02d}.jpg".format(fnroot,i)

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
            print("Renaming {} --> {}".format(src,dst))
            os.rename(src,dst)
            
        i+=1
