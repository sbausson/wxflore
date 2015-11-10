#!/usr/bin/env python2

import sys

bdtfx_path = sys.argv[-1]
sys.path.append(bdtfx_path)
#print(os.path.abspath(os.path.dirname(__file__)))
#/Intel/Home/Bot/Flores/Main/db/python/

import bdtfx

table = {}

for key in bdtfx.table:
    try:
        fam = bdtfx.table[key]["fam"]
        gen = bdtfx.table[key]["gen"]
        nl = bdtfx.table[key]["nl"]
    except:
        fam = ""
        gen = ""
        nl = ""

    if nl != "":
        if not item["fam"] in table.keys():
            table[item["fam"]] = {}
        if not item["gen"] in table[item["fam"]].keys():
            table[item["fam"]][item["gen"]] = {}


        

