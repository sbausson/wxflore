#!/usr/bin/env python3

import re
import os
import sys
import csv
#from catminat import *

import bdtfx_CN

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
conv_table = [
#    ['NOM_SCIENTIFIQUE','NL'],
##    ['code_CATMINAT','ID.cat'],
##    ['N°_Taxinomique_BDNFF','ID.bdnff'],

#    ["fréquence_absolue","freq.abs"],
#    ["fréquence_relative","freq.rel"],
    ["rareté_nationale","rar"],
##    ['CHOROLOGIE','ECO.ch'],
##    ['inflorescence','FL.inf'],
##    ['sexualité','FL.se'],
##    ['ordre_maturation','FL.mat'],
##    ['pollinisation','FL.pol'],
##    ['fruit','FL.fru'],
##    ['dissémination','FL.dis'],
##    ['couleur_fleur','FL.col'],
##    ['macule','FL.mac'],
##    ['floraison','FL.flo'],
##    ['type_ligneux','TL'],
##    ['Hauteur_végétative_maximum_[m]','Hmax'],
##    ['TYPE_BIOLOGIQUE','Tbio'],
##    ['FORMATION_VEGETALE','FV'],
##    ['CARACTERISATION_ECOLOGIQUE_(HABITAT_OPTIMAL)','ECO.opt'],
##    ['INDICATION_PHYTOSOCIOLOGIQUE_CARACTERISTIQUE','IPC'],
##    ['INDICATION_CARACTERISTIQUE_TRANSGRESSIVE','ICT'],
##    ['INDICATION_DIFFERENTIELLE_1','ID1'],
##    ['INDICATION_DIFFERENTIELLE_2','ID2'],
##    ['INDICATION_DIFFERENTIELLE_3','ID3'],
##    ['Lumière','GRAD.L'],
##    ['Température', 'GRAD.T'],
##    ['Continentalité','GRAD.C'],
##    ['Humidité_atmosphérique', 'GRAD.Ha'],
##    ['Humidité_édaphique','GRAD.He'],
##    ['Réaction_du_sol_(pH)','GRAD.pH'],
##    ['Niveau_trophique','GRAD.tro'],
##    ['Salinité','GRAD.sal'],
##    ['Texture','GRAD.tex'],
##    ['Matière_organique','GRAD.MO'],
#    ['ROYAUME_[ou_subroyaume_?]','CLA.ro'],
#    ['EMBRANCHEMENT_[division,_phylum]_(-phyta)','CLA.emb'],
#    ['SUBEMBRANCHEMENT_(-phytina)', 'CLA.sub_emb'],
#    ['CLASSE_(-opsida)','CLAS.cla'],
#    ['SUBCLASSE_(-idae)','CLA.sub_cla'],
#    ['Clade_intermédiaire', 'CLA.cla_int'],
#    # 'Clade_intermédiaire', 'Clade_intermédiaire',
#    ['SUPERORDRE_(-anae)','CLA.sup_ord'],
#    #'Clade_intermédiaire',
#    ['ORDRE_(-ales)','CLA.ord'],
#    ['FAMILLE_(-aceae)','CLA.fam'],

#    ['SUBFAMILLE_(-oideae)','CLA.sub_fam']
#    ['SECTION','CLA.sec'],
#    ['SUBSECTION','CLA.sub_sec '],
#    ['SERIE','CLA.ser']
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
def build_chorodep_python_module():

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
                CN = row[indexes.index("N°_Taxinomique_BDNFF")]

                try:
                    errro()
                    id = bdtfx_CN.table[CN]
                except:                    
                    id = row[indexes.index("N°_Nomenclatural_BDNFF")]
                    #print("## WARNING ## {}".format(id))

                if id in id_t:
                    print("Already in list",nl)
                else:
                    id_t.append(id)
                if id == "23244":
                    print("toto",nl)
                    
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

