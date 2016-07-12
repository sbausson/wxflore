#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re
import sys
import time, datetime
import types
import color
import codecs
import bota
import region

class PATHS:
    db = ""
    img = ""
    coste = ""
    #baseflor = ""
    catminat = ""
    bk = ""

class OPTIONS:
    desc = 0
    short = 0
    filename = "" #"/home/toto/Plantes/plantes.db.txt"
    force = 0
    coste = 0
    db_directory = ""
    html = 0
    sort = 0
    nyd = 0
    py = 0
    tag = ""
    total = 0
    verbose = 0
    update_file = 0 # to update NL in tela files
    more_directories = []
    warning = 0
    paths = PATHS()
    debug = 0

    class debug_infos:
        not_updated = 0
        chorodep = 0


key_list = ["NL","SY","NV",
            "N.DE","N.ES","N.NL","N.UK","N.IT","N.DE",
            "FA","OR","ZO","TM","DS","HB","TO","TG","CU","MD","US","PR","NT","FL",
            "CB","CD","DG","DA","BT",
            "CN","ID.coste","ID.tela","ID.inpn",
            "N.coste",
            "REF.wiki.fr",
            "FL.col",
            "XX"

]

line_parity = 0
cell_format = """<td bgcolor="%s" valign="top"><font color="%s">%s<br></td>"""


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def init():

    options = OPTIONS()
    options.log_filename = "wxflore.log"
    with open(options.log_filename,"w"):
        pass

    return options

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def warning(s,color,options):

    color_t = {
        "red":91,
        "green":92,
        "yellow":93,
        "blue":94,
        "magenta":95,
        "cyan":96,
        "white":98,
    }

    options.warning += 1
    print(u"\033[{}m{}\033[{}m".format(color_t[color],s,0))

    with codecs.open(options.log_filename,'a','utf-8') as f:
    #with open(options.log_filename,"a") as f:
        f.write(s+"\n")

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def expend_pattern(pattern):
    pattern = pattern.replace("a","[aáàâäÁÀÂÄ]")
    pattern = pattern.replace("e","[eéèêëÉÈÊË]")
    pattern = pattern.replace("i","[iíìïîÍÌÎÏ]")
    pattern = pattern.replace("o","[oóòöôÓÒÔÖ]")
    pattern = pattern.replace("u","[uúùüûÚÙÛÜ]")
    pattern = pattern.replace("c","[cçÇ]")
    return pattern

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def reduce_pattern(pattern):
    pattern = re.sub("[aáàâäÁÀÂÄ]","a",pattern)
    pattern = re.sub("[eéèêëÉÈÊË]","e",pattern)
    pattern = re.sub("[iíìïîÍÌÎÏ]","i",pattern)
    pattern = re.sub("[oóòöôÓÒÔÖ]","o",pattern)
    pattern = re.sub("[uúùüûÚÙÛÜ]","u",pattern)
    pattern = re.sub("[cçÇ]","c",pattern)
    return pattern

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_struct(line,struct,options):

    if options.verbose:
        print(line)

    try:
        keyword,value = line.split(":",1)
    except:
        print(line)
        ERROR()

    if keyword in key_list:
        struct[keyword] = value.strip()
    else:
        print("--->"+line+"<---")
        ERROR()

    return

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def display_struct(struct,compressed,i,options):

    global line_parity

    nl = struct["NL"]

    if "NV" not in struct:
        nv = ""
    else:
        nv = struct["NV"]


    if "N.UK" not in struct:
        nuk = ""
    else:
        nuk = struct["N.UK"]

    if "N.NL" not in struct:
        nnl = ""
    else:
        nnl = struct["N.NL"]

    if "N.ES" not in struct:
        nes = ""
    else:
        nes = struct["N.ES"]

    if "N.IT" not in struct:
        nit = ""
    else:
        nit = struct["N.IT"]

    if "N.DE" not in struct:
        nde = ""
    else:
        nde = struct["N.DE"]



    if "NE" not in struct:
        ne = ""
    else:
        ne = struct["NE"]

    if "SY" not in struct:
        sy = ""
    else:
        sy = struct["SY"]

    if "FA" not in struct:
        fa = ""
    else:
        fa = struct["FA"]

    if "ZO" not in struct:
        zo = ""
    else:
        zo = struct["ZO"]

    tg = ""
    #if struct.has_key("TG") and struct["TG"] == "y":
    #    tg = "***"
    #else:
    #    tg = ""


    if compressed == 1:
        if options.short == 2:
            s="%-20s %-50s %-50s" % (fa,nl,nv)
        elif options.short == 3:
            s="- {0} / {1}".format(nl.replace("[","").replace("]",""),nv)
        elif options.short == 4:
            s="- {0:70} {1}".format(nl,nv)
        else:
            s="\n"
            s+="[ %s ]\n" % struct["FN"]
            s+="-"*90
            s+="\n"
            s+="%-25s : %-50s %s\n" % ("Nom latin",nl,tg)

            # Nom vernaculaire
            nv_=nv.split(";")
            if len(nv_) == 1:
                s+="%-25s : %s\n" % ("Nom vernacualire",nv)
            else:
                s+="%-25s : %s\n" % ("Noms vernacualires",",".join(nv_))

            # Nom anglais
            if nuk != "":
                nuk_=nuk.split(";")
                if len(nuk_) == 1:
                    s+="%-25s : %s\n" % ("Nom anglais",nuk)
                else:
                    s+="%-25s : %s\n" % ("Noms anglais",",".join(nuk_))

            # NL
            if nnl != "":
                nnl_=nnl.split(";")
                if len(nnl_) == 1:
                    s+="%-25s : %s\n" % ("Nom Néerlandais",nnl)
                else:
                    s+="%-25s : %s\n" % ("Noms Néerlandais",",".join(nnl_))

            # ES
            if nes != "":
                nes_=nes.split(";")
                if len(nes_) == 1:
                    s+="%-25s : %s\n" % ("Nom Espagnol",nes)
                else:
                    s+="%-25s : %s\n" % ("Noms Espagnol",",".join(nes_))

            # IT
            if nit != "":
                nit_=nit.split(";")
                if len(nit_) == 1:
                    s+="%-25s : %s\n" % ("Nom Italien",nit)
                else:
                    s+="%-25s : %s\n" % ("Noms Italien",",".join(nit_))

            # DE
            if nde != "":
                nde_=nde.split(";")
                if len(nde_) == 1:
                    s+="%-25s : %s\n" % ("Nom Allemand",nde)
                else:
                    s+="%-25s : %s\n" % ("Noms Allemand",",".join(nde_))

            # Famille
            s+="%-25s : %s\n" % ("Famille",fa)
            if 0 and struct.has_key("CN") and struct["CN"] != "":
                print("%-25s : %s\n" % ("Code nomenclatural",struct["CN"]))

            if options.short == 0:
                # Synonyme
                if len(sy) == 1:
                    s+="{0:25} : {1}\n".format("Synonyme",', '.join(sy))
                elif len(sy) > 1:
                    s+="%-25s :\n" % ("Synonymes")
                    for syn in sy:
                        s+="\t- %s\n" % syn #s+="{0:25} : {1}\n".format("Synonyme(s)",', '.join(sy))

                if options.short in  [0,1]:
                    s+="%s :\n" % ("Description")
                    for ds in struct["DS"]:
                        s+="\t- %s\n" % ds


        #print "-"*90

            if options.short == 0:

                try:
                    s+="%-25s : %s\n" % ("Habitat",struct["HB"])
                except:
                    pass

                try:
                    s+="%-25s : %s\n" % ("Zone Géographique",struct["ZO"])
                except:
                    pass

                try:
                    s+="%-25s : %s\n" % ("Floraison",struct["FL"])
                except:
                    pass

                try:
                    s+="%-25s : %s\n" % ("Usage",struct["US"])
                except:
                    pass

                try:
                    if struct["true_coste"]:
                        c = color.GREEN
                    else:
                        c = color.RED

                    s+=color.scol("%-25s : N°%s " % ("Ref. Coste",struct["ID.coste"]),c)
                    s+=color.scol("({})".format(struct["N.coste"]),c)

                except:
                    pass

                s+="\n"

                if "ID.tela" in struct and struct["ID.tela"] != "":
                    s+="%-25s : N°%s  http://www.tela-botanica.org/bdtfx-nn-%s-synthese\n" % ("Ref. Tela",struct["ID.tela"],struct["ID.tela"])

                try:
                    s+="%-25s : N°%s  http://inpn.mnhn.fr/espece/cd_nom/%s\n" % ("Ref. INPN",struct["ID.inpn"],struct["ID.inpn"])
                    s+="%-25s : http://siflore.fcbn.fr/?cd_ref=%s&r=metro\n" % ("Répartition FCNB",struct["ID.inpn"])
                except:
                    pass

                try:
                    s+="%-25s : %s\n" % ("Wiki.Fr",struct["REF.wiki.fr"])
                except:
                    pass


        print(s) #.encode("utf-8"))

        #print "-"*90


    else:
        for key in key_list:
            if struct.has_key(key):
                print("{0}: {1}".format(key,struct[key]))
        print("")


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def filter_struct(struct,patterns,options):

    import unicodedata
    import string


    s=""
    for key in struct.keys():
        if isinstance(struct[key],str):
            s +=  struct[key]
        elif isinstance(struct[key],list):
            s += ''.join(struct[key])

    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))

    found = 1
    for pattern in patterns:
        if not re.search(pattern,s,re.I|re.U):
            found = 0
            break

    if options.tag != "":
        found = found and (struct["TG"].upper() == options.tag.upper())

    return found


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def print_total(struct):

    fam_t = {}
    n = 1

    tot = 0
    for key in struct.keys():
        try:
            fam = struct[key]["FA"]
        except:
            print(key)
            ERROR()

        if fam in fam_t:
            fam_t[fam] += 1
        else:
            fam_t[fam] = 1
        tot += 1

    print("-" * 150)
    l_full = sorted(fam_t.keys())

#    for fam_group in [l[x:x+n] for x in range(1, len(l), n)]:
#        print(''.join(["%25s : %3s" % (fam,fam_t[fam]) for fam in fam_group]))

    for letter in map(chr,range(ord('A'),ord('Z')+1)):
        l = [name for name in l_full if name[0] == letter]
        #print(len(l),l)
        if l != []:
            print()
            print(" [ {} ]".format(letter))
            for fam_group in [l[x:x+n] for x in range(0, len(l), n)]:
                print(''.join(["%22s : %3s" % (fam,fam_t[fam]) for fam in fam_group]))


#    split=[l[i:i+len(l)/num_cols] for i in range(0,len(l),len(l)//num_cols)]
#    print split
#    for row in zip(*split):
#        #print "".join(str.ljust(i,20) for i in row)
#        print row
#
#    for i in range (0,len(fam_sorted_list)/num_col):
#        print "%30s : %s" % (fam_sorted_list[i],fam_t[fam_sorted_list[i]])
    print("-" * 150)
    print(" Total = %s" % tot)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def handle_coste(struct,options):


    coste_list_files = os.listdir(options.paths.coste)
    coste_removed = [int(x.split(".")[0]) for x in coste_list_files if re.match("[0-9]+\.coste$",x)]

#    coste_removed = [210,273,
#                     1162,1170,1185,1190,
#                     3662,
#                     4254,4329]

    coste_t = [0]*4355

    tot = 0
    for key in struct.keys():
        if struct[key]["DS"] != [] and struct[key]["ID.coste"] != "":
            id_coste = int(struct[key]["ID.coste"])
            if id_coste not  in coste_removed:
                print(struct[key]["ID.tela"], end=" ")
                tot += 1

    print()
    print("-"*100," ",tot)

    tot = 0
    for key in struct.keys():

        try:
            coste_id = int(struct[key]["ID.coste"])
            coste_t[coste_id] = 1
        except:
            pass

    n=0
    s_res = ""
    s=""
    c_missing=[]
    for i in range(1,len(coste_t)):
        if not coste_t[i] and i not in coste_removed:
            c_missing.append(i)

    print("\nCoste reference missing: {}\n{}".format(n,c_missing))

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_argv(options):

    i = 1
    while i < len(sys.argv):

        if sys.argv[i] == "-update":
            options.update_data = 1

        elif sys.argv[i] == ".":
            options.more_directories.append(os.getcwd())

        elif sys.argv[i] in ["-ds","-des","-desc"]:
            options.desc = 1

        elif sys.argv[i] in ["-t","-total"]:
            options.total = 1

        elif sys.argv[i] in ["-coste"]:
            options.coste = 1

        elif sys.argv[i] == "-file":
            i+=1
            options.filename = sys.argv[i]

        elif sys.argv[i] == "-db":
            i+=1
            options.db_directory = sys.argv[i]

        elif sys.argv[i] == "-html":
            options.html = 1

        elif sys.argv[i] in ["-short","-s"]:
            options.short = 1

        elif sys.argv[i] in ["-ss"]:
            options.short = 2

        elif sys.argv[i] in ["-sss"]:
            options.short = 3

        elif sys.argv[i] in ["-l"]:
            options.short = 4

        elif sys.argv[i] in ["-nyd"]:
            options.nyd = 1
            options.args = sys.argv[i+1:]
            #options.nyd_file = sys.argv[i+1]
            #i+=1

        elif sys.argv[i] in ["-py"]:
            options.py = 1

        elif re.match("-tag=[ynYN]",sys.argv[i]):
            options.tag = sys.argv[i].split("=")[1].strip().upper()

        elif sys.argv[i] == "-verbose":
            options.verbose = 1

        else:
            return sys.argv[i:]

        i+=1

    return ""

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def nyd(filename,struct_table,options):

    in_list = []
    out_list = []

    f = open(filename)
    for line in f.readlines():
        if line.strip() != "":
            in_list.append(line.strip())

    for name in [struct['NL'] for struct in [struct_table[key] for key in struct_table.keys()]]:
        name_reduced = name.split("[")[0].strip()
        if name_reduced not in in_list:
            out_list.append(name_reduced)

    if options.args:
        expr = "\s*".join(options.args)
        print(expr)
        found = 0
        for name in in_list:
            if re.match(expr,name,re.I):
                print("Already done !")
                found = 1
                break
        if not found:
            for name in out_list:
                if re.match(expr,name,re.I):
                    print("Not yet DONE !")
                    found = 1
                    break

        if not found:
            print("Not in Database")

    else:
        n = 5
        z = [in_list[x:x+n] for x in range(0, len(in_list), n)]
        print("-"*100)
        print('\n'.join([''.join(s.rjust(35)for s in row) for row in z]))
        print("-"*100)
        z = [out_list[x:x+n] for x in range(0, len(out_list), n)]
        print('\n'.join([''.join(s.rjust(35)for s in row) for row in z]))
        print("-"*100)


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def python_table(base_flore_path,options=OPTIONS()):

    res_table = {}
    res_table_content = {}

    struct_table = {}
    fam_list = []
    gen_list = []

    filenames = [options.paths.db]

    path = os.path.join(options.paths.db,"python")
    print(sys.path)

    try:
        import bdtfx
        options.bdtfx = bdtfx
        print('Loading "bdtfx.py" ...')
    except:
        options.bdtfx = {}
        print("## WARNING ## : Can not load 'bdtfx' ...")

    try:
        import taxref
        options.taxref = taxref
        print('Loading "taxref.py" ...')
    except:
        print("## WARNING ## : Can not load 'taxref' ...")

    try:
        import baseflor
        options.baseflor = baseflor
        print('Loading "baseflor.py" ...')
    except:
        print('## WARNING ## : Can not load "baseflor.py" !')

    try:
        import chorodep
        options.chorodep = chorodep
        print('Loading "chorodep.py" ...')
    except:
        options.chorodep = {}
        print('## WARNING ## : Can not load "chorodep.py !')

    try:
        import baseveg
        options.baseveg = baseveg
        print('Loading "baseveg.py" ...')
    except:
        print('## WARNING ## : Can not load "baseveg.py !')


    # Import RED LIST
    #-----------------
    try:
        import redlist
        options.redlist_table = redlist.table
        print('Loading "redlist.py" ...')
    except:
        print('## WARNING ## : Can not load "redlist.py !')


    options.prot = {}
    # Import Protections (Nat,reg,dep)
    #----------------------------------
    for prot_type in ["nat","reg","dep"]:
        options.prot[prot_type] = {}
        dir_prot = os.path.join(options.paths.python,"prot",prot_type)
        sys.path.append(dir_prot)
        if os.path.exists(dir_prot):
            print("Loading prot/reg ",end="")
            for region in [fn.split(".")[0] for fn in os.listdir(dir_prot) if re.match(".*\.py$",fn)]:
                try:
                    #print(region)
                    import importlib
                    #mod = importlib.import_module("{}.{}.{}".format("prot","reg",region))
                    mod = importlib.import_module(region)
                    #options.prot[mod.name] = mod.liste
                    options.prot[prot_type][region] = mod.liste
                    print("'{}'".format(region),end=" ")

                except IOError:
                    print("error")
                    pass
            print()


    # Read 'Cat' files ...
    #----------------------
    options.cat = {}
    if os.path.exists(options.paths.cat):
        for fn in os.listdir(options.paths.cat):
            cat, ext = fn.split(".")
            if ext == "cat":
                print("Loading category \"{}\" ...".format(fn))
                cat  = cat.decode("utf8")
                options.cat[cat] = []
                f = open(os.path.join(options.paths.cat,fn),"r")
                for l in f.readlines():
                    id = l.strip()
                    if id != "":
                        options.cat[cat].append(id)
    #print(options.cat)

    # Read Taxon files
    #------------------
    for filename in filenames :
        print(filename)
        for root, dirs, files in os.walk(filename, topdown=False):
            for name in files:

                if re.match('[A-Z]',os.path.split(root)[-1][0]) and re.match("[A-Z][a-z]+\.[a-z_]+(\-)?[a-z_]*$",name):
                    filename = os.path.join(root, name)
                    struct_table[filename] = parse_file(filename,name,options)


    chorodep_counter=0
    photos_path_list = []
    for key in struct_table.keys():
        struct = struct_table[key]
        #print(key,struct.keys())
        name_reduced = bota.ReduceName(struct["NL"])
        photos_path_list.append(name_reduced)
        if struct['ID.tela'] != "" and struct['ID.tela'] in options.chorodep.table:
            chorodep_counter += 1

    # Check Catminat ID exists
    #--------------------------
    for key in struct_table.keys():
        if "baseflor" in struct_table[key].keys():
            if "ID.cat" in struct_table[key]["baseflor"]:
                id_cat =  struct_table[key]["baseflor"]["ID.cat"]
                if not id_cat in options.baseveg.table and id_cat != "inconnu":
                    warning(u"## WARNING ## Catminat ID '{}' not found for '{}' ...".format(id_cat,
                                                                                            struct_table[key]["NL"]),"blue",options)

    # Check orphan photos
    #---------------------
    if os.path.exists(os.path.join(options.paths.img,"photos")):
        for filename in  os.listdir(os.path.join(options.paths.img,"photos")):
            if filename not in photos_path_list:
                warning("## WARNING ## {} photo not linked to any taxon ...".format(filename),"magenta",options)

    print("="*50)
    print("chorodep count={}".format(chorodep_counter))

    return struct_table

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_file_telacol(filename,struct,options):

    import codecs

    try:
        f = codecs.open(filename,'r','utf-8')
        struct["telacol.DS"] = f.readlines()
        f.close()
        return
    except:
        sys.stderr.write("## WARNING {} ## \"{}\" Reading error ...\n".format(options.warning,filename))
        struct["telacol_ds"] = ""
        return

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_file_coste(coste_id,struct,options):

    import codecs
    filename = os.path.join(options.paths.coste,"{}.coste".format(coste_id))

    try:
        f = codecs.open(filename,'r','utf-8')
        content = f.readlines()
        struct["true_coste"] = 1
        f.close()
    except:
        sys.stderr.write("## WARNING {} ## \"{}\" Not found [ Tela {} ]...\n".format(options.warning,filename,struct["ID.tela"]))
        struct["true_coste"] = 0
        return

    struct["FN.coste"]  = filename

    i=0
    #print(content)
    while i < len(content):

        line = content[i]

        if line.strip() == "" or re.match('#',line):
            in_struct = 0
            if re.match('#',line):
                comments.append(line.strip())
            i+=1
        else:
            in_struct = 1

            try:
                keyword,value = line.split(":",1)
            except:
                print(filename)
                print(line)
                ERROR()


            if keyword == "DS":
                if value.strip() != "":
                    struct[keyword] = [x.strip() for x in value.split(";")]
                    i+=1
                else:
                    i+=1
                    struct[keyword] = []
                    while i < len(content) and not re.match("[A-Z]",content[i]):
                        value = content[i].strip()
                        if value[0] == "-":
                            value = value[1:].strip()
                        struct[keyword].append(value.strip())
                        i+=1

            elif keyword in ["N.coste","HB","ZO","FL","FR","US"]:
                struct[keyword] = value.strip()
                i+=1
            else:
                i+=1

    #print(content)
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_file_user(filename,struct,options):

    import codecs

    try:
        #filename = os.path.join(options.paths.meta,"flore.user",user_fn)
        f = codecs.open(filename,'r','utf-8')
        content = f.readlines()
        f.close()
        print("="*50)
        print("User {}".format(filename))
        print("="*50)
    except:
        sys.stderr.write("## WARNING {} ## \"{}\" Not found [ Tela {} ]...\n".format(options.warning,filename,struct["ID.tela"]))
        return

    i=0
    struct["user"] = {}
    #print(content)
    while i < len(content):

        line = content[i]

        if line.strip() == "" or re.match('#',line):
            in_struct = 0
            if re.match('#',line):
                comments.append(line.strip())
            i+=1
        else:
            in_struct = 1

            try:
                keyword,value = line.split(":",1)
            except:
                print(filename)
                print(line)
                ERROR()


            if keyword == "DS":
                if value.strip() != "":
                    struct["user"][keyword] = [x.strip() for x in value.split(";")]
                    i+=1
                else:
                    i+=1
                    struct["user"][keyword] = []
                    while i < len(content) and not re.match("[A-Z]",content[i]):
                        value = content[i].strip()
                        if value[0] == "-":
                            value = value[1:].strip()
                        struct["user"][keyword].append(value.strip())
                        i+=1

            elif keyword in ["HB","ZO","FR",]:
                struct["user"][keyword] = value.strip()
                i+=1
            else:
                i+=1

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_BOT(filename,struct,options):

    print(filename)

    import codecs

    f = codecs.open(filename,'r','utf-8')
    content = f.readlines()
    f.close()

    struct["bot"] = {}
    for line in content:
        if line.strip():
            try:
                keyword,value = line.split(":",1)
            except:
                print(line)
                error()

            if keyword == "FL.co":
                struct["bot"]["FL.co"] = value
                print("bot / FL.co")

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def __parse_BASEFLOR(filename,struct,options):

    #print(filename)

    import codecs

    f = codecs.open(filename,'r','utf-8')
    content = f.readlines()
    f.close()

    struct["baseflor"] = {}
    for line in content:
        if line.strip():
            try:
                keyword,value = line.split(":",1)
            except:
                print(line)
                error()

            struct["baseflor"][keyword] = value.strip()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_TAGS(filename,struct,options):

    tags_t = []
    f = codecs.open(filename,'r','utf-8')
    for line in f.readlines():
        tags_t+=[x.strip() for x in line.split(";")]

    struct["tags"] = tags_t

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_SEEALSO(filename,struct,options):

    t = []
    f = codecs.open(filename,'r','utf-8')
    for line in f.readlines():
        line = line.replace(",",";")
        t+=[x.strip() for x in line.split(";") if x.strip() != ""]

    struct["seealso"] = t

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def update_file(filename,nl):

    t = []
    with codecs.open(filename,'r','utf-8') as f:
        for l in f.readlines():
            if re.match("^NL:",l):
                l=u"NL: {}\n".format(nl)
            t.append(l)

    with codecs.open(filename,'w','utf-8') as f:
        for l in t:
            f.write(l)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#def parse_file(root,name,struct,options):
def parse_file(filename,name,options):

    #filename = os.path.join(root, name)

    #print(root)
    #print(name)
    #print(filename)

    f = codecs.open(filename,'r','utf-8')
    content = f.readlines()
    f.close()

    struct = {"NL":"",
              "NV":"",
              "DS":[],
              "ID.tela":"",
              "ID.coste":"",
              "chorodep":{},
              #"DESC":[],
    }

    comments = []
    in_struct = 0
    i=0

    #print(filename)
    while i < len(content):

        line = content[i]#.decode("utf-8")
        #print i,line.strip()

        if line.strip() == "" or re.match('#',line):

            in_struct = 0
            if re.match('#',line):
                comments.append(line.strip())
            i+=1
        else:
            in_struct = 1

            try:
                keyword,value = line.split(":",1)
                #value = value.decode('utf-8')
            except: # IOError:
                print(filename)
                print(line)
                ERROR()

            if keyword == "SY":
                if value.strip() != "":
                    struct[keyword] = [x.strip() for x in value.split(";")]
                    i+=1
                else:
                    i+=1
                    struct[keyword] = []
                    while i < len(content) and not re.match("[A-Z]",content[i]):
                        value = content[i].strip()
                        if value[0] == "-":
                            value = value[1:].strip()
                        struct[keyword].append(value.strip())
                        i+=1

            elif keyword == "DS":
                if value.strip() != "":
                    struct[keyword] = [x.strip() for x in value.split(";")]
                    i+=1
                else:
                    i+=1
                    struct[keyword] = []
                    while i < len(content) and not re.match("[A-Z]",content[i]):
                        value = content[i].strip()
                        if value[0] == "-":
                            value = value[1:].strip()
                        struct[keyword].append(value.strip())
                        i+=1

                #print "DS,%s:\n%s" % (keyword,struct["DS"])

            elif keyword in key_list:
                struct[keyword] = value.strip()
                i+=1
            else:
                i+=1
            #parse_struct(line,struct,options)

    if "ID.tela" in struct.keys() and struct["ID.tela"] != "":
        if struct["ID.tela"] in options.bdtfx.table.keys():
            #print(options.bdtfx[struct["ID.tela"]])
            #print(type(struct["NL"]),type(options.bdtfx[struct["ID.tela"]]["NL"]))
            #print(struct["NL"],options.bdtfx[struct["ID.tela"]]["NL"])

            struct["NL"] = struct["NL"].replace(u"×","x")

            if struct["NL"] != options.bdtfx.table[struct["ID.tela"]]["NL"]:
                options.debug_infos.not_updated += 1

                warning("\n## WARNING ## : ({}) {} does not seem uptodate ... {}\n{}\n{}".format(options.debug_infos.not_updated,
                                                                                                 struct["ID.tela"],
                                                                                                 filename,
                                                                                                 struct["NL"].encode("utf-8"),
                                                                                                 options.bdtfx.table[struct["ID.tela"]]["NL"].encode("utf-8")),"red",
                        options)
                struct["NL"] = unicode(options.bdtfx.table[struct["ID.tela"]]["NL"])
                if options.update_file:
                    resp = raw_input('Update "{}" ? (y/n) '.format(filename))
                    if resp == "y":
                        update_file(filename,struct["NL"])

            elif ("" != options.bdtfx.table[struct["ID.tela"]]["fam"] and
                  struct["FA"] != options.bdtfx.table[struct["ID.tela"]]["fam"]):
                warning("\n## WARNING ## : Familly mismatch ...\n{} {} -> {}".format(filename,struct["FA"],options.bdtfx.table[struct["ID.tela"]]["fam"]),
                        "cyan",
                        options)

            #struct["NL"] = unicode(options.bdtfx[struct["ID.tela"]]["NL"])
            #print(struct["NL"],filename) #options.bdtfx[struct["ID.tela"]])
            #print(filename)
#            for syn in options.bdtfx[struct["ID.tela"]]["syn"]:
#                try:
#                    syn_t.append(options.bdtfx[syn]["NL"])
#                except IOError:
#                    pass
#
            #print(syn_t)
            struct["SY"] = options.bdtfx.table[struct["ID.tela"]]["syn"]
            struct["ID.inpn"] = options.bdtfx.table[struct["ID.tela"]]["ID.inpn"]
            struct["bdtfx"] = options.bdtfx.table[struct["ID.tela"]]
        else:
            warning("{} not in bdtfx ... {}".format(struct["ID.tela"],filename),
                    "yellow",options)


    # COSTE Description file
    #------------------------
    if "ID.coste" in struct.keys() and "N.coste" not in struct.keys():
        for id in struct["ID.coste"].split(","):
            if struct["ID.coste"] != "":
                parse_file_coste(id,struct,options)


    # User Description file
    #-----------------------
    user_fn = os.path.join(options.paths.meta,"flore.user",name)
    if os.path.exists(user_fn):
        parse_file_user(user_fn,struct,options)

    try:
        telacol_fn = os.path.join(options.paths.telacol,"{}.tc".format(name.replace(".","_")))
        if os.path.exists(telacol_fn):
            parse_file_telacol(telacol_fn,struct,options)
    except:
        pass


    if hasattr(options.paths,"meta"):
        fn = os.path.join(options.paths.meta,"tags",name)
        if os.path.exists(fn):
            parse_TAGS(fn,struct,options)

    if hasattr(options.paths,"seealso"):
        fn = os.path.join(options.paths.seealso,name)
        if os.path.exists(fn):
            parse_SEEALSO(fn,struct,options)


    struct["cat"] = []
    if hasattr(options,"cat"):
        for cat in options.cat.keys():
            if struct["ID.tela"] in options.cat[cat]:
                struct["cat"].append(cat)

    # Catminat / baseflor
    #---------------------
    try:
        struct['baseflor'] = options.baseflor.table[struct["ID.tela"]]

    except:
        struct['baseflor'] = {}

    if "FL.col" in struct["baseflor"] and struct['baseflor']["FL.col"] != "":
        if "FL.col" in struct:
            warning("## WARNING ## 'FL.col' field ignored for '{}' ...".format(struct["NL"]),"red",options)
        else:
            struct["FL.col"] = struct['baseflor']["FL.col"]

    # Catminat / chorodep
    #---------------------
    try:
        struct["chorodep"] = options.chorodep.table[struct["ID.tela"]]
        #options.debug.chorodep+=1
    except:
        struct["chorodep"] = {}

    # Catminat / RedList
    #---------------------
    try:
        struct["redlist"] = options.redlist_table[struct["ID.tela"]]
    except:
        pass

    struct["prot.nat"] = []
    for key in options.prot["nat"].keys():
        if "ID.inpn" in struct.keys() and struct["ID.inpn"] in options.prot["nat"][key]:
            struct["prot.nat"].append(key) #.decode("utf8"))

    struct["prot.reg"] = []
    for key in options.prot["reg"].keys():
        if "ID.inpn" in struct.keys() and struct["ID.inpn"] in options.prot["reg"][key]:
            #and struct["ID.inpn"] not in options.prot["dep"][key]:
            struct["prot.reg"].append(key) #.decode("utf8"))

    struct["prot.dep"] = []
    for key in options.prot["dep"].keys():
        if "ID.inpn" in struct.keys() and struct["ID.inpn"] in options.prot["dep"][key]:
            reg = region.get_region(key)
            if reg in struct["prot.reg"]:
                struct["prot.reg"].remove(reg)

            struct["prot.dep"].append(key) #.decode("utf8"))

#    BOT_filename = os.path.join(options.db_base_dir,"data.BOT","{}.BOT".format(name))
#    if os.path.exists(BOT_filename):
#        print(options.db_base_dir)
#        parse_BOT(BOT_filename,struct,options)

    struct["N."] = name
    struct["nl"] = struct["NL"].replace("["," ").replace("]","")
    struct["FN"] = filename

    if struct["NL"] == "":
        print(filename)
        print(struct)
        error()

    return struct

#    if struct["NL"] != "":
#        struct_table[filename] = struct

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_files(pattern_list,options):

    struct_table_filtered = {}
    struct_table = {}
    patterns = []
    for pattern in pattern_list:
        patterns.append(expend_pattern(pattern))

    if options.db_directory == "":
        options.db_directory = os.path.join(os.path.abspath(os.path.dirname(__file__))[:-3],"fam")

    #options.db_base_dir = os.path.join(options.db_directory,"flores")
    #options.db_directory = os.path.join(options.db_base_dir,"flore.main")
    #options.coste_dir = os.path.join(options.db_base_dir,"flore.coste")

    locations = options.more_directories + [options.paths.db]
    print("locations={}".format(locations))

    try:
        import bdtfx
        options.bdtfx = bdtfx
        print('Loading "bdtfx.py" ...')
    except:
        print("## WARNING ## : Can not load 'bdtfx' ...")

    try:
        import baseflor
        options.baseflor = baseflor
        print('Loading "baseflor.py" ...')
    except:
        print('Can not load "baseflor.py" !')

    try:
        import chorodep
        options.chorodep = chorodep
        print('Loading "chorodep.py" ...')
    except:
        print('Can not load "chorodep.py !')

    try:
        import redlist
        options.redlist_table = redlist.table
        print('Loading "redlist.py" ...')
    except:
        print('Can not load "redlist.py !')

    for location in locations:

        for root, dirs, files in os.walk(location, topdown=False):
            for name in files:
                if re.match("[A-Z][a-z]+\.[a-z_]+(\-)?[a-z_]*$",name):

                    try:
                        filename = os.path.join(root, name)
                        struct_table[filename] = parse_file(filename,name,options)
                    except IOError:
                        print(root,name)
                        error()


    if options.total:
        print_total(struct_table)

    elif options.coste:
        handle_coste(struct_table,options)

    elif options.nyd:
        bfdf_fn = os.path.join(options.db_directory.split("Flore.db")[0],"Flore.db","bfdf.txt")
        nyd(bfdf_fn,struct_table,options)

    elif options.py:
        python_table(struct_table)

    else:
        for key in struct_table.keys():
            if filter_struct(struct_table[key],patterns,options):
                struct_table_filtered[key] = struct_table[key]

        i = 0
        key_list = sorted(struct_table_filtered.keys())
        for key in key_list:
            i+=1
            try:
                #print(key)
                display_struct(struct_table_filtered[key],1,i,options)
            except:
                print(key)
                ERROR()


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    options = OPTIONS()
    pattern_list = parse_argv(options)

    #db_base_dir = os.path.join(options.db_directory,"flores")
    db_base_dir = os.path.join(options.db_directory,"db")

    print(db_base_dir)

    options.paths.db = os.path.join(db_base_dir,"flore.main")
    options.paths.coste = os.path.join(db_base_dir,"flore.coste")
    options.paths.telacol = os.path.join(db_base_dir,"flore.telacol")
    options.paths.seealso = os.path.join(db_base_dir,"see.also")
    options.paths.cat = os.path.join(db_base_dir,"cat")

    options.paths.meta = os.path.join(options.db_directory,"meta")

    sys.path.append(os.path.join(db_base_dir,"python"))

    parse_files(pattern_list,options)
