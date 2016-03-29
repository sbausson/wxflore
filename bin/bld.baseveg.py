#!/usr/bin/env python3

import re
import os
import sys
import csv

#import bdtfx_CN

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def bld_filename(nl):

    n = nl
    n = n.replace(" subsp. ","-")
    n = n.replace(" var. ","-")
    try:
        name = re.findall("([A-Z][a-zë\- ]*)",n)[0]
    except:
        print(nl)
        error()

    name = name.strip().replace(" x ",".").replace(" ",".")
    if len(name.split(".")) == 1:
        name = ""
        print("## WARNING ## Ignoring : {}".format(nl))

    return name

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
conv_table = [
    ['SYNTAXON','SYNTAXON'],
    ['NIVEAU','level'],
    ['Dénomination écologique','ECO.name'],
    ['Chorologie mondiale','choro.world'],
    ['Répartition connue \nen France','REP.fr'],
    ['Physionomie', 'C.physio'],
    ['Etages altitudinaux\n (altitude)','C.alti'],
    ['Latitude','C.lat'],
    ['Océanité','C.ocea'],
    ['Température','C.temp'],
    ['Lumière','C.lum'],
    ['Exposition, pente','C.exp'],
    ['Optimum \nde développement','C.opt'],
    ['Humidité \natmosphérique','C.humi.nat'],
    ["Types de sol et d'humus",'C.humus'],
    ['Humidité \nédaphique','C.humi.ned'],
    ['Texture \ndu sol','C.tex'],
    ['Niveau \ntrophique','C.niv.troph'],
    ['pH du sol','C.pH'],
    ['Salinité','C.sal'],
    ['Dynamique','C.dyn'],
    ['Influences \nanthropozoogènes','C.infl'],
]

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def build_python_module():

    baseflor_filename = sys.argv[-1]
    try:
        version=re.findall("baseveg\-(.*).csv",baseflor_filename)[0]
    except:
        print("Version can not be detected ...  Exiting !")
        sys.exit()

    filename = "baseveg-{}.py".format(version)
    f = open(filename,"w")


    f.write('# -*- coding: utf-8 -*-\n')
    f.write('\n#keys# = Code Catminat\n\n')

    f.write("version='{}'\n\n".format(version))
    f.write("table={\n")
    with open(baseflor_filename, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        i=0

        for row in reader:
            if i == 0:
                indexes=row
                print(indexes)
            else:
                id_cat = row[indexes.index("CODE \nCATMINAT")]
                niv = row[indexes.index("NIVEAU")]
                #CN = row[indexes.index("N°_Taxinomique_BDNFF")]
                #print(row)

                if niv in ['ALL',
                           'ASS',
                           'ASSGR',
                           'CLA','SUBCLA',
                           'ORD','SUBORD',
                           'SUBALL',
                ]:

                    s=''
                    s+='"{}":'.format(id_cat)
                    s+='{'

                    for item in conv_table:

                        s+='"{}": "{}",'.format(item[1],row[indexes.index(item[0])].replace('\n',' ').replace('"',"'"))
                    f.write(s)

                    s_=[]
                    for i in range(0,len(indexes)):
                        dep_match=re.match(".*\((.*)\)",indexes[i])
                        if dep_match:
                            ndep = dep_match.group(1)
                            x = row[i].strip()
                            if x in ["1"]:
                                s_.append(ndep)
                            elif x not in ["1?","-|-","-|-?","#","#?","?","<",""]:
                                print(i)
                                print(x)
                                print(row)
                                error()
                    f.write('"1": {}'.format(sorted(s_)))
                    f.write('},\n')

                elif re.match("[0-9]{2}/$",id_cat):
                    #print(row[indexes.index("SYNTAXON")])
                    name = row[indexes.index("SYNTAXON")].split("(")[0].strip()
                    s='"{}":{{"ECO.name":"{}"}}'.format(id_cat,name)
                    f.write(s+",\n")
                    #print(s)

            i+=1


    f.write("}\n")
    f.close()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
build_python_module()
