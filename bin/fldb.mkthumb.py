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
if __name__ == '__main__':

    wxflore_bin_path = os.path.join(os.path.split(os.path.abspath(__file__))[0],"..","wxflore-x.x")
    sys.path.append(wxflore_bin_path)

    import mkthumb

    options = OPTIONS()
    parse_argv(options)

    if options.local:
        flore_img_path = os.getcwd()
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

    mkthumb.mkthumb(options,flore_img_path)
