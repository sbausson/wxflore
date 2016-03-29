#!/usr/bin/env python2

import re
import os
import sys
import csv
import codecs

#from catminat import *

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
conv_table = [
    ["num_nom","num_nom"],
    ["num_nom_retenu","num_nom_retenu"],
    ["nom_sci","nom_sci"],
    ["auteur","auteur"],
    ["annee","annee"],
    ["cd_nom","cd_nom"],

]

table = {}
nl_t = {}

fam_t = {}
gen_t = {}

class OPTIONS:
    type = 0

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_argv(options):

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-2":
            options.type = 2

        elif i == (len(sys.argv) - 1):
            options.filename = sys.argv[-1]

        i+=1

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
options = OPTIONS()
parse_argv(options)

bdtfx_in_file = sys.argv[-1]
try:
    version=re.findall("bdtfx_(v[1-9]_[0-9]+)_ref.txt",bdtfx_in_file)[0]
except:
    print("Version can not be detected ...  Exiting !")
    sys.exit()

filename = "bdtfx_{}.py".format(version)

#f = open(filename,"w")
f = codecs.open(filename,'w','utf-8')

with open(bdtfx_in_file, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
    i=0
    for row in reader:
        if i == 0:
            i+=1
            indexes=row
            print(indexes)
        else:
            #print(row)
            if options.type == 2:
                num = row[indexes.index("Num\xc3\xa9ro nomenclatural")]
                num_ref = row[indexes.index("Num\xc3\xa9ro nomenclatural du nom retenu")]
                sup_ref = row[indexes.index("Num\xc3\xa9ro nomenclatural rang sup\xc3\xa9rieur")]
                num_basio = row[indexes.index("Num\xc3\xa9ro du basionyme")]
                name_sci = row[indexes.index("Nom sans auteur")]
                genre = row[indexes.index("Genre")]
                rang = int(row[indexes.index("Code rang")])
                author = row[indexes.index("Auteur")]
                author_date = row[indexes.index("Ann\xc3\xa9e publication")]
                id_inpn = row[indexes.index("Num\xc3\xa9ro INPN")]
            else:
                num = row[indexes.index("num_nom")]
                num_ref = row[indexes.index("num_nom_retenu")]
                sup_ref = row[indexes.index("num_tax_sup")]
                num_basio = row[indexes.index("num_basionyme")]
                name_sci = row[indexes.index("nom_sci")]
                genre = row[indexes.index("genre")]
                rang = int(row[indexes.index("rang")])
                author = row[indexes.index("auteur")]
                author_date = row[indexes.index("annee")]
                id_inpn = row[indexes.index("cd_nom")]

            s = "{}".format(name_sci)
            if author.strip() != "" and author_date.strip() != "":
                s += " [{}, {}]".format(author,author_date)
            elif author.strip() != "":
                s += " [{}, {}]".format(author,author_date)
                #s += " [{}]".format(author,author_date)

            nl = s.decode("utf-8")
            nl_t[num] = nl

            if name_sci == "toto":
                print("num_ref",num_ref)
                print("sup_ref",sup_ref)
                print("rang",rang)
                print("num",num)
                error()

            if num_ref != "":
                if num_ref not in table.keys():
                    table[num_ref] = {"syn.id":[]}

                if rang == 180:
                    if name_sci == "Caryophyllaceae":
                        print(name_sci,num_ref)
                        print(row)
                    fam_t[num_ref] = name_sci

                elif rang == 220 and sup_ref != "":
                    if re.match("Dianthus",name_sci):
                        print(name_sci,num_ref)
                        print(row)
                    gen_t[name_sci] = sup_ref

                elif num != num_ref:
                    table[num_ref]["syn.id"].append(num)

                elif num_ref != "":
                    table[num_ref]["NL"] = nl
                    table[num_ref]["ID.inpn"] = id_inpn
                    table[num_ref]["gen"] = genre


#f.write("'{}':{}\n".format(num_ref,table[num_ref]))
f.write("# -*- coding: utf-8 -*-\n")
f.write("version='{}'\n".format(version))
f.write("table={\n")
for key in table.keys():
    #print(table[key])
    if key != "":
        table[key]["syn"] = []
        for i in range(0,len(table[key]["syn.id"])):
            table[key]["syn"].append(nl_t[table[key]["syn.id"][i]])

        try:
            print(table[key]["gen"])
            print(gen_t[table[key]["gen"]])
            #print(fam_t[gen_t[table[key]["gen"]]])
            table[key]["fam"] = fam_t[gen_t[table[key]["gen"]]]
        except:
            table[key]["fam"] = ""

        #print(table[key])

        f.write("'{}':{},\n".format(key,table[key]))
f.write("}\n")
f.close()
