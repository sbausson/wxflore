#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import re
import sys
import time, datetime
import types

class STRUCT:
    firstname = ""
    lastname = ""
    email  = ""
    tel    = []
    mobile = []
    coreid = ""
    unixid = ""
    misc = ""
    
class OPTIONS:
    desc = 0
    short = 0
    filename = "" #"/home/toto/Plantes/plantes.db.txt"
    db_directory = ""
    html = 0
    sort = 0
    tag = ""
    total = 0
    verbose = 0

key_list = ["NL","SY","NV",
            "N.DE","N.ES","N.NL","N.UK",
            "FA","CN","OR","ZO","TM","DS","HB","TO","TG","CU","MD","US","PR","NT","FL",
            "CB","CD","DG","DA","BT",
            "ID"]

line_parity = 0
cell_format = """<td bgcolor="%s" valign="top"><font color="%s">%s<br></td>"""

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
        print line

    try:
        keyword,value = line.split(":",1)
    except:
        print line
        ERROR()

    if keyword in key_list:
        struct[keyword] = value.strip()    
    else:
        print "--->"+line+"<---"

        ERROR()

    return

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def display_struct(struct,compressed,i,options):

    global line_parity
    
    nl = struct["NL"]    
    
    if not struct.has_key("NV"):
        nv = ""
    else:
        nv = struct["NV"]

    if not struct.has_key("NE"):
        ne = ""
    else:
        ne = struct["NE"]

    if not struct.has_key("SY"):
        sy = ""
    else:
        sy = struct["SY"]
        
    if not struct.has_key("FA"):
        fa = ""
    else:
        fa = struct["FA"]
        
    if not struct.has_key("ZO"):
        zo = ""
    else:
        zo = struct["ZO"]

    tg = ""
    #if struct.has_key("TG") and struct["TG"] == "y":
    #    tg = "***"
    #else:
    #    tg = ""
        
    if options.html:
        if line_parity == 0:
            color = "#ccccff"
        else:
            color = "#ffccff"
        line_parity = (line_parity + 1) % 2
        
        print """<tr>"""
        #print nv,len(nv)
        #print nv.decode("utf-8")
        #print nv.encode("utf-8"),len(nv.decode("utf-8"))
        #print cell_format % (color,"#000000",nl.decode("utf-8").encode("latin-1"))
        #print cell_format % (color,"#000000",nv.decode("utf-8").encode("latin-1"))
        print cell_format % (color,"#000000",i)
        print cell_format % (color,"#000000",nl)
        print cell_format % (color,"#000000",sy.replace(";","<br>"))
        print cell_format % (color,"#000000",nv.replace(";","<br>"))
        print cell_format % (color,"#000000",ne.replace(";","<br>"))
        print cell_format % (color,"#000000",fa)
        print cell_format % (color,"#000000",zo)
        print """</tr>"""

    elif compressed == 1:
        if options.short == 2:
            s="%-20s %-50s %-50s" % (fa,nl,nv)
        else:
            s="\n"
            s+="[ %s ]\n" % struct["FN"]
            s+="-"*90
            s+="\n"
            s+="%-25s : %-50s %s\n" % ("Nom latin",nl,tg)
            #print nv
            s+="%-25s : %s\n" % ("Nom(s) vernacualire(s)",nv)
            if sy != "":
                s+="%-25s : %s\n" % ("Synonyme(s)",sy)
            s+="%-25s : %s\n" % ("Famille",fa)
            if 0 and struct.has_key("CN") and struct["CN"] != "":
                print "%-25s : %s\n" % ("Code nomenclatural",struct["CN"])
        
        #print "-"*90

            if options.short == 0:
                s+="%-25s :\n" % ("Description")
                for ds in struct["DS"]:
                    s+="\t- %s\n" % ds
                
                try:
                    s+="%-25s : %s\n" % ("Habitat",struct["HB"])
                except:
                    pass

                try:
                    s+="%-25s : %s\n" % (u"Zone Géographique",struct["ZO"])
                except:
                    pass
            
        print s.encode("utf-8")

        #print "-"*90

        
    else:
        for key in key_list:
            if struct.has_key(key):
                print "%s: %s" % (key,struct[key])
        print

    
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def filter_struct(struct,patterns,options):

    s=""
    for key in struct.keys():
        if type(struct[key]) == types.StringType:
            s+=struct[key]
        elif type(struct[key]) == types.ListType:
            s+=''.join(struct[key])
    
    found = 1
    for pattern in patterns:
	if not re.search(pattern,s,re.IGNORECASE):
	    found = 0
	    break

    if options.tag != "":
        #print struct["NL"]
        found = found and (struct["TG"].upper() == options.tag.upper())
        
    return found


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def print_total(struct):

    fam_t = {}
    n = 3

    tot = 0
    for key in struct.keys():
        try:
            fam = struct[key]["FA"]
        except:
            print key
            ERROR()

        if fam_t.has_key(fam):
            fam_t[fam] += 1
        else:
            fam_t[fam] = 1
        tot += 1

    print "-" * 150
    l = sorted(fam_t.keys())
    for fam_group in [l[x:x+n] for x in xrange(1, len(l), n)]:
        print ''.join(["%25s : %3s" % (fam,fam_t[fam]) for fam in fam_group])
        

#    split=[l[i:i+len(l)/num_cols] for i in range(0,len(l),len(l)//num_cols)]
#    print split
#    for row in zip(*split):
#        #print "".join(str.ljust(i,20) for i in row)
#        print row
#
#    for i in range (0,len(fam_sorted_list)/num_col):
#        print "%30s : %s" % (fam_sorted_list[i],fam_t[fam_sorted_list[i]])
    print "-" * 150
    print " Total = %s" % tot

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_argv(options):

    i = 1
    while i < len(sys.argv):

        if sys.argv[i] == "-update":
            options.update_data = 1

        elif sys.argv[i] in ["-ds","-des","-desc"]:
            options.desc = 1

        elif sys.argv[i] in ["-t","-total"]:
            options.total = 1

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
def __parse_file(filename,struct_table):
    
    f = open(filename,"r")
    comments = []
    
    in_struct = 0
    for line in f.xreadlines():
        if line.strip() == "" or re.match('#',line):
            if in_struct:
                struct_table[filename] = struct
                                    
            in_struct = 0
            if re.match('#',line):
                comments.append(line.strip())
    
        else: 
            if not in_struct:
                struct = {"DS":[]}
            in_struct = 1
            parse_struct(line,struct,options)    

    struct["FN"] = filename
    struct_table[filename] = struct

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_file(filename,struct_table):
    
    import codecs

    #f = open(filename,"r")
    f = codecs.open(filename,'r','utf-8')
    content = f.readlines()
    f.close()

    comments = []
    in_struct = 0
    i=0

    #print filename
    while i < len(content):
        
        line = content[i] #.decode("utf-8")
        #print i,line.strip()

        if line.strip() == "" or re.match('#',line):
            if in_struct:
                struct_table[filename] = struct
                                    
            in_struct = 0
            if re.match('#',line):
                comments.append(line.strip())
            i+=1
        else: 
            if not in_struct:
                struct = {"DS":[]}
            in_struct = 1
            
            try:
                keyword,value = line.split(":",1)
                #value = value.decode('utf-8')
            except IOError:
                print filename
                print line
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

                #print "DS,%s:\n%s" % (keyword,struct["DS"])

            elif keyword in key_list:
                struct[keyword] = value.strip()    
                i+=1
            else:
                i+=1
            #parse_struct(line,struct,options)    

    struct["FN"] = filename
    struct_table[filename] = struct

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_files(options):


    struct_table_filtered = {}
    struct_table = {}
    patterns = []
    for pattern in pattern_list:
        patterns.append(expend_pattern(pattern))

    if options.db_directory == "":
        options.db_directory = os.path.join(os.path.abspath(os.path.dirname(__file__))[:-3],"fam")

    if options.db_directory != "":
                
        for root, dirs, files in os.walk(options.db_directory, topdown=False):
            for name in files:
                if re.match("[A-Z][a-z]+\.[a-z_]+(\-)?[a-z_]*$",name):
                    full_filename = os.path.join(root, name)
                    parse_file(full_filename,struct_table)
                    #print name

            #for name in dirs:
            #    print("2",os.path.join(root, name))

    if options.total:
        print_total(struct_table)
        return

    if options.sort:
        sorted_list = struct_table.keys()
        sorted_list.sort()
        for key in sorted_list:
            display_struct(struct_table[key],0,i,options)
        for line in comments:
            print line
    else:        
        for key in struct_table.keys():
            if filter_struct(struct_table[key],patterns,options):
                struct_table_filtered[key] = struct_table[key]

    i = 0
    key_list = struct_table_filtered.keys()
    key_list.sort()
    for key in key_list:
        i+=1
        try:
            #print key
            display_struct(struct_table_filtered[key],1,i,options)
        except:
            print key
            ERROR()

    
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

options= OPTIONS()
try:
    file = open(os.environ["HOME"]+"/.pldb/options","r")
    execfile(os.environ["HOME"]+'/.pldb/options')
except (IOError,KeyError):
    pass

pattern_list = parse_argv(options)

if options.html:
    print """<?xml version="1.0" encoding="UTF-8"?>"""
    print """<html>"""
    print """<head>"""
    print """<title></title>"""
    print """</head>"""    
    print """<body bgcolor="#ffffff" text="#000000">"""    
    print """<br>"""
    print """<br>"""
    print """<table border="0" cellpadding="2" cellspacing="2" width="100%">"""
    print """<tbody>"""

if options.html:

    print "Dernière modification le %s" % datetime.date.today()
    print "<br>"
    print "Contact : sbausson@gmail.com"
    print "<br>"
    print "<br>"
    print """<tr>"""
    print cell_format % ("#333333","#ffcc00","#")
    print cell_format % ("#333333","#ffcc00","Nom latin")
    print cell_format % ("#333333","#ffcc00","Synonymes")
    print cell_format % ("#333333","#ffcc00","Nom vernaculaire")
    print cell_format % ("#333333","#ffcc00","English name")
    print cell_format % ("#333333","#ffcc00","Famille")
    print cell_format % ("#333333","#ffcc00","Zone")
    print """</tr>"""
        
parse_files(options)
if options.html:
    print """</tbody>"""
    print """</table>"""    
    print """<br>"""
    print """<br>"""
    print """</body>"""
    print """</html>"""
    
    
