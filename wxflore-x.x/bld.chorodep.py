#!/usr/bin/env python3

import re
import os
import sys
import csv

sys.path.append(os.getcwd())
import bdtfx

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
conv_table = [
    ["rareté_nationale","rar"],
]

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def build_chorodep_files():

    with open(sys.argv[-1], "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i=0
        for row in reader:
            if i == 0:
                i+=1
                indexes=row
                print(indexes)
            else:
                nl = row[indexes.index("NOM_SCIENTIFIQUE")]
                id = row[indexes.index("N°_Taxinomique_BDNFF")]
                if nl != "" and id != "":
                    filename = bld_filename(nl)

                    if filename != "":
                        s_ = []
                        f = open(os.path.join("chorodep",filename),"w")
                        for item in conv_table:
                            f.write("{}: {}\n".format(item[1],row[indexes.index(item[0])]))
                        for i in range(0,len(indexes)):
                            dep_match=re.match(".*\((.*)\)",indexes[i])
                            if dep_match:
                                ndep = dep_match.group(1)
                                x = row[i].strip()
                                if x in ["1"]: #,"1?"]:
                                    s_.append(ndep)
                                elif x not in ["1?","-|-","-|-?","#","#?","?",""]:
                                    print(x)
                                    error()
                        f.write("1: {}\n".format(";".join(sorted(s_))))
                        f.close()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def read_bdtfx():

    table = {}

    for key in bdtfx.table.keys():
        for syn_id in bdtfx.table[key]["syn.id"]:
            table[syn_id] = key

    return table

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def build_chorodep_python_module():

    bdtfx_syn_table = read_bdtfx()

    filename = "chorodep.py"
    f = open(filename,"w")

    csv_fn = sys.argv[-1]
    version = re.findall("chorodep-(.*)\.csv",csv_fn)[0]

    f.write("# -*- coding: utf-8 -*-\n")
    f.write("version='{}'\n".format(version))
    f.write("table={\n")

    id_t = []

    with open(csv_fn, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i=0

        for row in reader:
            if i == 0:
                i+=1
                indexes=row
                print(indexes)
            else:
                nl = row[indexes.index("NOM_SCIENTIFIQUE")]
                #id = row[indexes.index("N°_Taxinomique_BDNFF")]
                id = row[indexes.index("N°_Nomenclatural_BDNFF")]
                if id == '41864':
                    print(nl)

                if id not in ["nc"]:
                    if id not in bdtfx.table.keys():
                        try:
                            id = bdtfx_syn_table[id]
                        except:
                            id = ""

                    if id in id_t:
                        print("Already in list",nl)
                    else:
                        id_t.append(id)


                if nl != "" and not id in["","nc"]:
                    s = ""
                    s_ = []

                    s+='"{}":'.format(id)
                    s+='{'
                    for item in conv_table:
                        s+='"{}": "{}",'.format(item[1],row[indexes.index(item[0])])
                    f.write(s)

                    for i in range(0,len(indexes)):
                        dep_match=re.match(".*\((.*)\)",indexes[i])
                        if dep_match:
                            ndep = dep_match.group(1)
                            x = row[i].strip()
                            if x in ["1"]: #,"1?"]:
                                s_.append(ndep)
                            elif x not in ["1?","-|-","-|-?","#","#?","?",""]:
                                print(x)
                                error()
                    f.write('"1": {}'.format(sorted(s_)))
                    f.write("},\n")

    f.write("}\n")
    f.close()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
build_chorodep_python_module()
