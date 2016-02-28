#!/usr/bin/env python3

import sys
import os
import subprocess

class OPTIONS:
    local = 0
    config = ""
    noconfig = 0
    dumplicates = 0
    remove = 0
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

        elif sys.argv[i] == "-dup":
            options.duplicates = 1

        elif sys.argv[i] == "-remove":
            options.remove = 1

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

    mkthumb.mkthumb(options)
    if options.duplicates:
        mkthumb.check_all_duplicate(options)
