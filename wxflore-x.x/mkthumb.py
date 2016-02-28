#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import subprocess
import os
import re
import subprocess
import hashlib

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def download(options,subdir,link):

    dir = os.path.join(options.paths.img,"photos",subdir)
    cmd = 'wget -P {} "{}"'.format(dir,link)
    print(cmd)
    p = subprocess.call(cmd, shell=True)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def number(options,subdir):

    import sys

    print("mkthumb.number()")

    dir = os.path.join(options.paths.img,u"photos",subdir).encode('utf8')
    n=1

    for src in os.listdir(dir):

        if re.match(subdir + "\.[0-9]{2}.jpg",src):
            print("Name OK : {}".format(src))
        else:
            first = 1

            while first or os.path.exists(os.path.join(dir,dst)):
                first = 0
                dst = "{}.{:02d}.jpg".format(subdir,n)
                n+=1
                #print(n)

            if isinstance(src,unicode):
                s=u"Renaming {} --> {}".format(src,dst)
                print(s) #.encode('utf8','surrogateescape'))
            elif isinstance(src,str):
                s=u"Renaming {} --> {}".format(src.decode('utf8',errors='ignore'),dst)
                print(s.encode('utf8','surrogateescape'))
            else:
                error()

            os.rename(os.path.join(dir,src),os.path.join(dir,dst))

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def setdefault(options,subdir,filename):

    dir = os.path.join(options.paths.img,"photos",subdir)
    thumb_dir = os.path.join(options.paths.img,"photos.thumb",subdir)

    name_00 = "{}.00.jpg".format(subdir)

    if name_00 != filename:
        if os.path.exists(os.path.join(dir,name_00)):
            name_tmp = "{}.tmp".format(filename)
            os.rename(os.path.join(dir,name_00),os.path.join(dir,name_tmp))
            os.rename(os.path.join(dir,filename),os.path.join(dir,name_00))
            os.rename(os.path.join(dir,name_tmp),os.path.join(dir,filename))

            os.remove(os.path.join(thumb_dir,name_00))
            os.remove(os.path.join(thumb_dir,filename))
        else:
            os.rename(os.path.join(dir,filename),os.path.join(dir,name_00))

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def check_duplicate(options,subdir):

    res_t = []
    sha1_t = []

    for fn in sorted(os.listdir(os.path.join(options.paths.img,"photos",subdir))):
        fpath = os.path.join(options.paths.img,"photos",subdir,fn)

        # SHA1
        with open(fpath, 'rb') as f:
            sha1 = hashlib.sha1(f.read()).hexdigest()
            if sha1 in  sha1_t:
                res_t.append(fpath)
            else:
                sha1_t.append(sha1)

    return res_t

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def check_all_duplicate(options):

    for directory in os.listdir(os.path.join(options.paths.img,"photos")):
        for photo in check_duplicate(options,directory):
            if options.remove:
                print('Removing "{}" ...'.format(photo))
                os.remove(photo)
            else:
                print('This photo is a duplicate "{}" ...'.format(photo))

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def mkthumb(options,subdir=""):

    for directory in os.listdir(os.path.join(options.paths.img,"photos")):

        if subdir == "" or (subdir != "" and directory == subdir):
            photo_directory = os.path.join(options.paths.img,"photos",directory)
            thumb_directory = os.path.join(options.paths.img,"photos.thumb",directory)
            if not os.path.exists(thumb_directory):
                print("Creating {} ...".format(thumb_directory))
                os.makedirs(thumb_directory)

            #print("a",photo_directory)
            #print("b",thumb_directory)

            photo_list = []
            for filename in os.listdir(photo_directory):
                #print(filename)


                photo_list.append(filename)
                photo_filename = os.path.join(photo_directory,filename)
                thumb_filename = os.path.join(thumb_directory,filename)


#                # SHA1
#                with open(photo_filename, 'rb') as f:
#                    print(hashlib.sha1(f.read()).hexdigest())


                if not os.path.exists(thumb_filename):
                    print("Thumbing {} ...".format(thumb_filename))
                    # command
                    cmd = "convert -auto-orient -quality 75 -resize 200x200 %s %s" % (photo_filename,thumb_filename)
                    print(cmd)
                    #p = subprocess.Popen(cmd, shell=True)  #stdout=subprocess.PIPE)
                    p = subprocess.call(cmd, shell=True)  #stdout=subprocess.PIPE)

            # Clean orphan thumbnails
            #-------------------------
            for filename in os.listdir(thumb_directory):
                if filename not in photo_list:
                    thumb_filename = os.path.join(thumb_directory,filename)
                    print("Remove {} ...".format(thumb_filename))
                    os.remove(thumb_filename)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    class options:
        class paths:
            img = "/Bota/Flores/Main/img"

    number(options,"Lathyrus_palustris")
