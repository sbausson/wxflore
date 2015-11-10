#!/usr/bin/env python3

import sys
import os
import subprocess

class OPTIONS:
    local = 0
    
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_argv(options):

    i = 1
    while i < len(sys.argv):

        if sys.argv[i] == "-local":
            options.local = 1

        i+=1
        
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
options = OPTIONS()
parse_argv(options)

if options.local:
    flore_img_path = os.getcwd() #os.path.join("photos/img")
else:
    if os.getenv("HOME") == None:
        home  = os.getenv("HOMEPATH")
    else:
        home = os.getenv("HOME")            
    
    sys.path.append(os.path.join(home,".wxflore"))
    
    try:
        import config
        flore_img_path = config.flore_img_path
    except:
        print("Can not load flore_img_path ...")
        sys.exit()
        
#print(flore_img_path)

for directory in os.listdir(os.path.join(flore_img_path,"photos")):
    photo_directory = os.path.join(flore_img_path,"photos",directory)
    thumb_directory = os.path.join(flore_img_path,"photos.thumb",directory)
    if not os.path.exists(thumb_directory):
        print("Creating {} ...".format(thumb_directory))
        os.mkdir(thumb_directory)

    for filename in os.listdir(photo_directory):
        photo_filename = os.path.join(photo_directory,filename)
        thumb_filename = os.path.join(thumb_directory,filename)
        if not os.path.exists(thumb_filename):
            print("Thumbing {} ...".format(thumb_filename))
            # command
            cmd = "convert -auto-orient -quality 75 -resize 200x200 %s %s" % (photo_filename,thumb_filename)
            print(cmd)
            #p = subprocess.Popen(cmd, shell=True)  #stdout=subprocess.PIPE)
            p = subprocess.call(cmd, shell=True)  #stdout=subprocess.PIPE)

