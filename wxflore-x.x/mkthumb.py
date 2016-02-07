import subprocess
import os
import re
import subprocess

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def download(options,subdir,link):

    dir = os.path.join(options.paths.img,"photos",subdir)
    cmd = "wget -P {} {}".format(dir,link)
    print(cmd)
    p = subprocess.call(cmd, shell=True)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def number(options,subdir):

    print("mkthumb.number()")

    dir = os.path.join(options.paths.img,"photos",subdir)
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
                print(n)

            print("Possible filename : {} {}".format(src,dst))
            os.rename(os.path.join(dir,src),os.path.join(dir,dst))

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def setdefault(options,subdir,filename):

    dir = os.path.join(options.paths.img,"photos",subdir)
    thumb_dir = os.path.join(options.paths.img,"photos.thumb",subdir)

    name_00 = "{}.00.jpg".format(subdir)

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
def mkthumb(options,subdir=""):



#    if subdir != "":
#        photo_dir = os.path.join(options.paths.img,"photos",subdir)
#        thumb_dir = os.path.join(options.paths.img,"photos.thumb",subdir)
#        dirs=(photo_dir,thumb_dir)
#    else:
#    for directory in dirs:
#        print("-",directory)
#
#        photo_directory = os.path.join(options.paths.img,"photos",directory)
#        thumb_directory = os.path.join(options.paths.img,"photos.thumb",directory)


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
