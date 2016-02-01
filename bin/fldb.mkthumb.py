#!/usr/bin/env python3

import sys
import os
import subprocess

class OPTIONS:
    local = 0
    config = ""
    noconfig = 0
    class paths:
        pass

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

    if os.getenv("HOME") == None:
        options.home  = os.getenv("HOMEPATH")#.decode(sys.stdout.encoding)
    else:
        options.home = os.getenv("HOME")#.decode(sys.stdout.encoding)

    options.wxflore = os.path.join(options.home,".wxflore")

    if options.local:
        options.img = os.getcwd()
    else:
        import config
        config.read(options)



#        if os.getenv("HOME") == None:
#            home  = os.getenv("HOMEPATH")
#        else:
#            home = os.getenv("HOME")
#
#        sys.path.append(os.path.join(home,".wxflore"))
#
#        try:
#            import config
#            flore_img_path = config.flore_img_path
#        except:
#            print("Can not load flore_img_path ...")
#            sys.exit()

    mkthumb.mkthumb(options)
