#!/usr/bin/env python3

import os
import re
import shutil
import sys

class OPTIONS:
    force = 0
    
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_file(fn,options):

    import subprocess
    
    if os.path.getsize(fn) == 0:
        print('"{0}" is empty ! ...'.format(fn))                
        return 

    f = open(fn)
    for l in f.readlines():
        if re.match("FA: ",l):
            fam = l.split(':')[1].strip().upper()
            #print("{0} {1}".format(fn,fam.upper()))
            if os.path.isdir(fam):
                print('Move "{0}" to {1}/ ...'.format(fn,fam))
                path=os.path.join(fam.upper(),fn)
                
                if os.path.exists(path):
                    if options.force:
                        os.remove(path)
                    else:
                        print("Overwritting %s not completed" % path)
                        print("-"*150)
                        subprocess.call('sdiff {} {}'.format(fn,path), shell=True)
                        break
                
                #print(path)
                shutil.move(fn,fam.upper())
            else:
                print('You need to create directory "{0}/" ...'.format(fam))

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_argv(options):

    i = 1
    while i < len(sys.argv):

        if 0:
            pass

        elif sys.argv[i] in ["-f","-force"]:
            options.force = 1

        
        i+=1

    return ""

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
options = OPTIONS()
parse_argv(options)

dirs = os.listdir(".")
for fn in dirs:
    if os.path.isfile(fn) and re.match("[A-Z][a-z]+\.[a-z]*",fn):
        parse_file(fn,options)
