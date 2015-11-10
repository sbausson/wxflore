#!/usr/bin/env python2

import os
import sys
import subprocess

size = 1000
if len(sys.argv) == 2:
    ext = "xx"
    link = sys.argv[-1]
elif len(sys.argv) == 3:
    ext = sys.argv[-2]
    link = sys.argv[-1]
else:
    error()
    

for file in [fn]:
    cmd = "wget {}".format(link)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    
#    print "Reducing \"%s\" ..." % file
#    cmd = "convert -auto-orient -quality 75 -resize %sx%s %s x%s-%s" % (size,size,file,size,file)
#    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

    
