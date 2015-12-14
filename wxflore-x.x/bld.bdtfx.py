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

bdtfx_in_file = sys.argv[-1]
try:
    version=re.findall("bdtfx_(v3_[0-9]+)_ref.txt",bdtfx_in_file)[0]
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
            num = row[indexes.index("num_nom")]
            num_ref = row[indexes.index("num_nom_retenu")]
            sup_ref = row[indexes.index("num_tax_sup")]
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


            if num_ref != "":
                if num_ref not in table.keys():
                    table[num_ref] = {"syn":[]                              
                                  }
                
                if rang == 180:
                    fam_t[num_ref] = name_sci
                
                elif rang == 220 and sup_ref != "":
                    gen_t[name_sci] = sup_ref
                    
                elif num != num_ref:
                    table[num_ref]["syn"].append(num)
                
                else:
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
        for i in range(0,len(table[key]["syn"])):
            table[key]["syn"][i] = nl_t[table[key]["syn"][i]]

#        if table[key]["fam"] not in ["","0"]:
#            print(table[key])
#            table[key]["fam"] = nl_t[table[key]["fam"]]


        try:
            #print(table[key]["gen"])
            #print(gen_t[table[key]["gen"]])
            #print(fam_t[gen_t[table[key]["gen"]]])
            table[key]["fam"] = fam_t[gen_t[table[key]["gen"]]]
        except:
            table[key]["fam"] = ""

        #print(table[key])

        f.write("'{}':{},\n".format(key,table[key]))
f.write("}\n")
f.close()
