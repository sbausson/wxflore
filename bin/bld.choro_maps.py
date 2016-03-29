#!/usr/bin/env python3

import re
import os
import sys
import subprocess

sys.path.insert(0,os.getcwd())
import chorodep

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def build_map(identifier,list_of_depts,buffer):

    #print(identifier)

    re_dep = re.compile('\s*<path id="FR-([0-9][0-9AB])')
    with open("toto.svg","w") as g:
        for line in buffer:
            if re_dep.match(line):
                dep = re_dep.findall(line)[0]
                if dep in list_of_depts or (dep in ['2A','2B'] and '20' in list_of_depts):
                    g.write(line.replace('"land"','"active"'))
                else:
                    g.write(line)
            else:
                g.write(line)

    cmd_rsvg = "rsvg-convert -b '#99bbff' -o {}.png {}.svg".format("toto","toto")
    #print(cmd_rsvg)
    p = subprocess.call(cmd_rsvg, shell=True)

    cmd_convert ="gm convert -resize 200x200 {}.png {}".format("toto",os.path.join("choro.map",identifier+".png"))
    #print(cmd_convert)
    p = subprocess.call(cmd_convert, shell=True)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
buffer = []
with open("template.svg","r") as f:
    for l in f.readlines():
        buffer.append(l)

i = 0
n = len(chorodep.table.keys())
for key in chorodep.table:
    print("\r{}/{}".format(i,n),end="")
    build_map(key,
              chorodep.table[key]["1"],
              buffer)
    i+=1
