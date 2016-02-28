#!/usr/bin/env python3

import os
import re
import subprocess
import difflib
import filecmp
import sys

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def clean_file(filename):

    print(filename)

    f = open(filename,"r")
    g = open("{}.new".format(filename),"w")

    while 1:

        line = f.readline()
        if not line:
            break

        l_ = line.strip().split(":",1)

        if l_[0] in ["N.UK","N.DE","N.ES","N.IT","N.NL"]:
            line = "{}: {}".format(l_[0],"; ".join([x.strip().capitalize() for x in l_[1].replace(",",";").split(";")]))
            g.write(line+"\n")

        elif  l_[0] in ["NL","NV","N.US","N.CAT","N.ARB",
                      "ZO","FA","FL","HB","ID.tela","ID.coste","REF.wiki.fr","ID.inpn","ID.fona"]:
            g.write(line)

        elif l_[0] == "SY":
            while 1:
                line = f.readline()
                if not line or re.match("[A-Z].*:",line):
                    break
            if line != "":
                g.write(line)

        elif l_[0] in "N.coste":
            pass

        else:
            print(line)
            erro()

    f.close()
    g.close()

    #file1 = open(filename)
    #file2 = open("{}.new".format(filename))

    #diff = difflib.unified_diff(file1.readlines(), file2.readlines())
    #for l in diff:
    #    sys.stdout.write(l)

    new_filename = "{}.new".format(filename)
    if filecmp.cmp(filename,new_filename):
        os.remove(new_filename)
    else:
        print("-"*50)
        cmd = "colordiff -y {} {}.new".format(filename,filename)
        p = subprocess.Popen(cmd, shell=True)
        p.wait()
        print("-"*50)

        force = 0
        if force == 0:
            print("Replace {} ?".format(filename),end=" ")
            r = input()

        if force or r in ["o","O","y","Y"]:
            os.rename(new_filename,filename)
        else:
            pass

            #os.waitpid(p.pid, 0)


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
location = "/home/git/wxflore/Flores/Main/db/flore.main"

i = 0

for root, dirs, files in os.walk(location, topdown=False):
    for name in files:
        if re.match("[A-Z][a-z]+\.[a-z_]+(\-)?[a-z_]*$",name):

            filename = os.path.join(root, name)
            clean_file(filename)
            i+=1
