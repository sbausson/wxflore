#!/usr/bin/env python2

import os
import sys

i = 1
try:
    size = int(sys.argv[i])
    i+=1
except:
    size = 1000

for file in sys.argv[i:]:
    print "Reducing \"%s\" ..." % file
    command = "convert -auto-orient -quality 80 -resize %sx%s %s x%s-%s" % (size,size,file,size,file)
    os.system(command)
