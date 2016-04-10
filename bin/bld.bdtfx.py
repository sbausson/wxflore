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

                #Bonnier_num = row[indexes.index("Autres : flore_bonnier_num")]
                #Bonnier_rem = row[indexes.index("Autres : flore_bonnier_rem")]
                #CNRS_num = row[indexes.index("Autres : flore_cnrs_num")]
                #CNRS_rem = row[indexes.index("Autres : flore_cnrs_rem")]
                #FE_num = row[indexes.index("Autres : flore_fe_num")]
                #FE_rem = row[indexes.index("Autres : flore_fe_rem")]

                Coste_num = row[indexes.index("Autres : flore_coste_num")]
                Fournier_num = row[indexes.index("Autres : flore_fournier_num")]
                FB_num = row[indexes.index("Autres : flore_belge_ed5_page")]
                FG_num = row[indexes.index("Autres : flore_fg_num")]
                #if FB_num == "0644 R":
                #    print(row)
                    #error()
                #print(FB_num)
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

            if num_ref != "":
                if num_ref not in table.keys():
                    table[num_ref] = {}
                    table[num_ref]["syn.id"] = []
                    table[num_ref]["rang"] = rang

                    table[num_ref]["Coste_num"] = ""
                    table[num_ref]["Coste_name"] = ""
                    table[num_ref]["Coste_syn"] = []

                    table[num_ref]["Fournier_num"] = ""
                    table[num_ref]["Fournier_name"] = ""
                    table[num_ref]["Fournier_syn"] = []

                    table[num_ref]["FG_num"] = ""
                    table[num_ref]["FG_name"] = ""
                    table[num_ref]["FG_syn"] = []

                    table[num_ref]["FB_num"] = ""
                    table[num_ref]["FB_name"] = ""
                    table[num_ref]["FB_syn"] = []

                    if Coste_num != "":
                        if len(Coste_num.split(".")) > 1:
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["Coste_syn"].append(name_sci)
                        else:
                            table[num_ref]["Coste_num"] = Coste_num
                            table[num_ref]["Coste_name"] = name_sci

                    if Fournier_num != "":
                        if len(Fournier_num.split(".")) > 1:
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["Fournier_syn"].append(name_sci)
                        else:
                            table[num_ref]["Fournier_num"] = Fournier_num.decode('utf-8')
                            table[num_ref]["Fournier_name"] = name_sci

                    if FG_num != "":
                        if FG_num[-1] != "r":
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["FG_syn"].append(name_sci)
                        else:
                            table[num_ref]["FG_num"] = FG_num[:-1]
                            table[num_ref]["FG_name"] = name_sci

                    if FB_num != "":
                        if FB_num[-1] != "R":
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["FB_syn"].append(name_sci)
                        else:
                            table[num_ref]["FB_num"] = FB_num[:-1].strip()
                            table[num_ref]["FB_name"] = name_sci


                if rang == 180:
                    fam_t[num_ref] = name_sci

                elif rang == 220 and sup_ref != "":
                    gen_t[name_sci] = sup_ref

                elif num != num_ref:
                    table[num_ref]["syn.id"].append(num)

                    if Fournier_num != "":
                        if len(Fournier_num.split(".")) > 1:
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["Fournier_syn"].append(name_sci)
                        else:
                            table[num_ref]["Fournier_num"] = Fournier_num.decode('utf-8')
                            table[num_ref]["Fournier_name"] = name_sci

                    if FG_num != "":
                        if FG_num[-1] != "r":
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["FG_syn"].append(name_sci)
                        else:
                            table[num_ref]["FG_num"] = FG_num[:-1]
                            table[num_ref]["FG_name"] = name_sci

                    if FB_num != "":
                        if FB_num[-1] != "R":
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["FB_syn"].append(name_sci)
                        else:
                            table[num_ref]["FB_num"] = FB_num[:-1].strip()
                            table[num_ref]["FB_name"] = name_sci

                # Remove
                #   220 = genre
                #
                elif num_ref != "" and rang not in [220]:
                    table[num_ref]["NL"] = nl
                    table[num_ref]["ID.inpn"] = id_inpn
                    table[num_ref]["gen"] = genre
                    table[num_ref]["rang"] = rang

                    #table[num_ref]["CNRS_num"] = CNRS_num
                    #table[num_ref]["CNRS_rem"] = CNRS_rem
                    #table[num_ref]["FE_num"] = FE_num
                    #table[num_ref]["FE_rem"] = FE_rem
                    #table[num_ref]["Bonnier_num"] = Bonnier_num
                    #table[num_ref]["Bonnier_rem"] = Bonnier_rem
                    #table[num_ref]["Coste_num"] = Coste_num
                    #table[num_ref]["Fournier_num"] = Fournier_num
                    #table[num_ref]["FB_num"] = FB_num
                    #table[num_ref]["FG_num"] = FG_num

                    if Coste_num != "":
                        if len(Coste_num.split(".")) > 1:
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["Coste_syn"].append(name_sci)
                        else:
                            table[num_ref]["Coste_num"] = Coste_num
                            table[num_ref]["Coste_name"] = name_sci

                    if Fournier_num != "":
                        if len(Fournier_num.split(".")) > 1:
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["Fournier_syn"].append(name_sci)
                        else:
                            table[num_ref]["Fournier_num"] = Fournier_num.decode('utf-8')
                            table[num_ref]["Fournier_name"] = name_sci

                    if FG_num != "":
                        if FG_num[-1] != "r":
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["FG_syn"].append(name_sci)
                        else:
                            table[num_ref]["FG_num"] = FG_num[:-1]
                            table[num_ref]["FG_name"] = name_sci

                    if FB_num != "":
                        if FB_num[-1] != "R":
                            #table[num_ref]["Coste_num"] = Coste_num.split(".")[0]
                            table[num_ref]["FB_syn"].append(name_sci)
                        else:
                            table[num_ref]["FB_num"] = FB_num[:-1].strip()
                            table[num_ref]["FB_name"] = name_sci


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
            #print(table[key]["gen"])
            #print(gen_t[table[key]["gen"]])
            #print(fam_t[gen_t[table[key]["gen"]]])
            table[key]["fam"] = fam_t[gen_t[table[key]["gen"]]]
            table[key]["fam"] = ""
        except:
            table[key]["fam"] = ""

        #print(table[key])

        if "NL" in table[key]:
            f.write("'{}':{},\n".format(key,table[key]))
        elif table[key]["rang"] not in [180,220]:
            print("Skipping {}, {}".format(key,table[key]))

f.write("}\n")
f.close()
