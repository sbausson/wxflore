#!/usr/bin/env python3
# -*- coding: utf-8 -*-

divisions=[
    ["Andreaeopsida",["Andreaeaceae"]
    ],

    ["Bryopsida",["Bryaceae",
                  "Mniaceae"]
    ],

    ["Polytrichopsida",["Polytrichaceae"]],

    ["Sphagnopsida",["Sphagnaceae",
                     "Ambuchananiaceae"]
    ],


]

title = "Bryophytes"
default_division = "Sphagnopsida"


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    print(sum([div[1] for div in divisions],[]))
