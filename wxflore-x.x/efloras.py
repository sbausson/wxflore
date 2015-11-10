#!/usr/bin/env python3

import codecs
import sys
import re
import color

class OPTIONS:
    split_coste = 1
    flora = 1
    verbose = 0    

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def bota_name(s):

    #print(s)
    #m = re.match("(\×? ?[A-Z][a-z\.\-\× ]*)([A-Z\(][a-zA-Z,\.\&\-éèàö\) ]*)?\[?([0-9]*).*",s,re.UNICODE)
    m = re.match("(\×? ?[A-Z][a-z\.\-\× ]*)([A-Z\(][^\[]*)?\[?([0-9]*).*",s,re.UNICODE)
    #print(re.findall("((\× )?[A-Z][a-z\.\-\× ]*)([A-Z\(][a-zA-Z\.\)ö ]*)?\[?([0-9]*).*",s,re.UNICODE))
    try:
        s_ = m.groups()
        #print(s_)
        
        if len(s_) == 3:
            if s_[1] != None:
                return "{} [{}, {}]".format(s_[0].strip(),s_[1].strip(),s_[2].strip())
            else:
                return s_[0]
    except:
        pass
    
    print("Bota Name unparsed : {}\n".format(s))
    return None

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_fona(s,html,options):
    #f = codecs.open(sys.argv[-1],'r','utf-8')
    #f = open(filename, encoding='ISO-8859-1')
    
    in_desc = 0
    i = 0
    print(html)
    for line in html.split("\n"): #f.readlines():
        line = line.strip()
        
        if (in_desc == 0) and re.match('<span id="lblTaxonDesc">',line):
            in_desc = 1
        elif in_desc == 1:
            if re.match("</span>",line):
                in_desc = -1
            else:
                line = line.replace("<p><p>","\n")
                line = re.sub('<[^>]*>', '', line).strip()
                if line == "":
                    pass
                elif i == 0:
                    x = re.findall("([A-Z][a-z ]*) ([A-Z.\(][A-Za-z\(\). ]*).* ([0-9]{4})\. ",line)[0]
                    #print("NL: {} [{}, {}]".format(x[0],x[1],x[2]))
                    s.nl = "{} [{}, {}]".format(x[0],x[1],x[2])
                    i+=1

                    if options.verbose:
                        print(" --> Nom latin = {}".format(s.nl))
                        
                elif i == 1:
                    n_us = re.sub('<[^>]*>', '', line).strip()
                    s.nus = "; ".join([x.title() for x in n_us.split(",")])
                    i+=1
                    
                    if options.verbose:
                        print(" --> Nom US: {}".format(s.nus))
                              
                elif i == 2:
                    #print("SY: {}".format(line))
                    s.sy = re.sub('<[^>]*>', '', line).strip()
                    i+=1
                              
                    if options.verbose:
                        print(" --> Syn. : {}".format(s.sy))

                elif i == 3:
                    #print("DS:")
                    #print("\n".join(["- {}".format(x) for x in line.split(". ")]))
                    s.ds = "\n".join(["- {}".format(x) for x in line.split(". ")])
                    i+=1

                    if options.verbose:
                        print(" --> Description. : {}".format(s.ds))                    
                    
                elif i == 4:
                    fl,temp = line.split(".",1)
                    hb,hg,temp = temp.split(";",2)
                    if re.match("\s*introduced",temp):
                        zo,temp = temp.split(";",1)

                    print(line)
                    print("1",hb)
                    print("2",hg)
                    print ("3",temp)
                    
                    s.fl = fl.split()[1].strip()
                    s.hb = hb.strip()
                    s.hg = hg.strip()
                    s.zo = zo.strip()
                    s.zg = temp.strip()
                    i+=1
                elif i == 5:
                    s.oi = []
                    s.oi.append(line)
                    i+=1
                else:
                    s.oi.append(line)

    #print("OI:")
    #print("\n".join(oi))

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def read_file(s,filename,options):
    
    f = open(filename)
    html = "".join(f.readlines())
    parse_fona(s,html,options)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def read_url(s,id,options):

#    import urllib.request
#    response = urllib.request.urlopen('http://python.org/')
#    html = response.read()

    import urllib.parse
    import urllib.request

    #url = "http://www.tela-botanica.org/bdtfx-nn-{}-{}".format(id,content)
    
    if options.flora == 1:
        url = "http://www.efloras.org/florataxon.aspx?flora_id=1&taxon_id={}".format(id)
    elif options.flora == 5:
        url = "http://www.efloras.org/florataxon.aspx?flora_id=5&taxon_id={}".format(id)
        
    sys.stderr.write("{}\n".format(url))
    
    values = {}
    
#    data = urllib.parse.urlencode(values)
#    data = data.encode('utf-8') # data should be bytes
    req = urllib.request.Request(url) #, data)
    response = urllib.request.urlopen(req)
    page = response.read()
    #html = page.decode("iso-8859-1")
    html = page.decode()

    #print(html)
    s.id_fona = id
    parse_fona(s,html,options)
    
#    p = MyHTMLParser()
#    p.reset()
#    p.feed(page)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def parse_argv(options):

    i = 1
    while i < len(sys.argv):

        if sys.argv[i] == "-fona":
            options.flora = 1

        elif sys.argv[i] == "-fop":
            options.flora = 5

        elif sys.argv[i] == "-verbose":
            options.verbose = 1
            
        else:
            options.ids = sys.argv[i:]

        i+=1
        
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------

#url = "http://www.tela-botanica.org/bdtfx-nn-{}-synthese".format(sys.argv[-1])
#url = "http://www.tela-botanica.org/eflore/consultation/service.php?referentiel=bdtfx&niveau=2&module=fiche&action=onglet&num_nom={}&type_nom=&nom=&onglet=description".format(sys.argv[-1])

options = OPTIONS()
parse_argv(options)

print(options.ids)
for id in options.ids:    
    class s:
        hb=""
        zo=""
        ds=""
        fl=""
        fr=""
        nv=""
        us=""
        id_coste = ""
        n_coste = ""
        syn = []


#    read_file(s,sys.argv[-1])

    read_url(s,id,options)
#    read_url(s,id,"description")
#    read_url(s,id,"nomenclature")

    name = "{}.efloras".format(id)
    sys.stderr.write(color.scol("Writting \"{}\" ...\n".format(name),color.YELLOW))
    f = open(name,"w")
    
    f.write("NL: {}\n".format(s.nl))
    f.write("N.US: {}\n".format(s.nus))
    f.write("SY: {}\n".format(s.sy))
    f.write("ID.efloras: {}\n".format(s.id_fona))
    f.write("DS:\n{}\n".format(s.ds))
    f.write("FL: {}\n".format(s.fl))
    f.write("HB: {}\n".format(s.hb))
    f.write("HG: {}\n".format(s.hg))    
    f.write("ZG: {}\n".format(s.zg))    
    f.write("OI:\n{}\n".format("\n".join(s.oi)))
        
    f.close()            
    
    print("-"*50)
    f = open(name)
    for line in f.readlines():
        print(line,end="")
    if options.split_coste and s.id_coste != "":
        f.close()
        print("-"*100)
        f = open(name_coste)
        for line in f.readlines():
            print(color.scol(line,color.GREEN),end="")
        
    print("-"*100)



#-fop 200015975
