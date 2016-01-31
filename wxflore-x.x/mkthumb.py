import subprocess
import os

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def mkthumb(options,img_path):

    for directory in os.listdir(os.path.join(img_path,"photos")):
        photo_directory = os.path.join(img_path,"photos",directory)
        thumb_directory = os.path.join(img_path,"photos.thumb",directory)
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

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
