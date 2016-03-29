#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import os
import sys
import csv
import codecs


#from catminat import *

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def reduce_name(name):

    #print(name)
    #m = re.match("(\×? ?[A-Z][a-z\.\-\× ]*)([A-Z\(][a-zA-Z,\.\&\-éèàö\) ]*)?\[?([0-9]*).*",s,re.UNICODE)
    #print(type(name),name)
    m = re.match(u"(\×? ?[A-Z][a-z\.\-\× ]*)([A-Z\'\(][^\[]*)?\[?([0-9]*).*",name,re.UNICODE)
    #m = re.match(u"([A-Z][a-z\.\-\× ]*)([A-Z\'\(][^\[]*)?\[?([0-9]*).*",name,re.UNICODE)
    #print(re.findall("((\× )?[A-Z][a-z\.\-\× ]*)([A-Z\(][a-zA-Z\.\)ö ]*)?\[?([0-9]*).*",s,re.UNICODE))
    try:
        #print(name,m)
        s_ = m.groups()
        
        if len(s_) == 3:
            if s_[1] != None:
                return u"{}".format(s_[0].strip())
            else:
                #print(type(s_[0]))
                return s_[0]
    except IOError:
        pass
    
    print("Bota Name unparsed : {}\n".format(name))
    return None

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def get_inpn_in_bdtfx(name):

    name = name.decode("utf8")

    sys.path.append(os.path.join(os.getcwd(),"bdtfx"))
    import bdtfx
    rname = reduce_name(name)
    #print(rname)
    for key in bdtfx.table.keys():
        #print(bdtfx.table[key])
#        if bdtfx.table[key].has_key("NL"):
#            print(bdtfx.table[key]["NL"].split("[")[0].strip(),rname)

        if bdtfx.table[key].has_key("NL") and rname == bdtfx.table[key]["NL"].split("[")[0].strip():
            return bdtfx.table[key]["ID.inpn"]

    print(u"not found : {}".format(name))
    return name

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
conv_table = [
    ["num_nom","num_nom"],
    ["num_nom_retenu","num_nom_retenu"],
    ["nom_sci","nom_sci"],
    ["auteur","auteur"],
    ["annee","annee"],
    ["CD_NOM","CD_NOM"],
]
    

name_conv_table = {"Alsace":u"Alsace",
                   "Aquitaine":u"Aquitaine",
                   "Auvergne":u"Auvergne",
                   "Basse-Normandie":u"Basse-Normandie",
                   "Bourgogne":u"Normandie",
                   "Bretagne":u"Bretagne",
                   "Centre":u"Centre",
                   "Champagne-Ardenne":u"Champagne-Ardenne",
                   "Corse":u"Corse",
                   "Franche-Compte":u"Franche-Compté",
                   "Haute-Normandie":u"Haute-Normandie",
                   "IDF":u"Île-de-France",
                   "Languedoc-Roussillon":u"Languedoc-Roussillon",
                   "Limousin":u"Limousin",
                   "Lorraine":u"Lorraine",
                   "Midi-Pyrenees":u"Midi-Pyrénées",
                   "Nord-Pas-de-Calais":u"Nord-Pas-de-Calais",
                   "Pays-de-la-Loire":u"Pays-de-la-Loire",
                   "Picardie":u"Picardie",
                   "Poitou-Charentes":u"Poitou-Charentes",
                   "PACA":u"Provence-Alpes-Côte-d'Azur",
                   "Rhone-Alpes":u"Rhône-Alpes",
                   "France":"France"}

for csv_filename in sys.argv[1:]:
    liste = []
    py_root = csv_filename.rsplit(".")[0]
    py_filename = "{}.py".format(py_root)
    f = codecs.open(py_filename,'w','utf-8')

    with open(csv_filename, "r") as csvfile: 
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        i=0
        for row in reader:
            if i == 0:
                i+=1
                indexes=row
            else:
                id_inpn = row[-1]
                if id_inpn == "0":
                    id_inpn = get_inpn_in_bdtfx(row[indexes.index("Valide Name")])
                liste.append(id_inpn)
    
    print("Writting '{}' ...".format(py_filename))
    f.write("# -*- coding: utf-8 -*-\n")
    #f.write(u"name=u\"{}\"\n".format(name_conv_table[py_root]))
    f.write("liste=")
    f.write("{}".format(liste))
    f.write("\n")
    f.close()
