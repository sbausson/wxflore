#!/usr/bin/env python3

import codecs
import sys
import re
import color

class OPTIONS:
    debug = 0


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
    
    if options.debug:
        print(html)

    in_desc = 0
    i = 0
    html = html.replace("<p>","\n<p>\n")
    for line in html.split("\n"): #f.readlines():
        line = line.strip()
        
        if (in_desc == 0) and re.match('<span id="lblTaxonDesc">',line):
            in_desc = 1
        elif in_desc == 1:
            if re.match("</span>",line):
                in_desc = -1
            elif re.match("<p>",line,re.I):
                i+=1
                print("/",i)
            else:

                #line = line.replace("<p><p>","\n")
                line = re.sub('<[^>]*>', '', line).strip()

                if line == "":
                    if i == 1:
                        i+=1

                elif i == 0:
                    if options.debug:
                        print("if == 0:\n",line)
                    nl = line.split(".",1)[1].strip()
                    if options.debug:
                        print(nl)
                    x = re.findall("([A-Z][a-z ]*) (.*),.* ([1-9][0-9]{3})\.$",nl)[0]
                    #print("NL: {} [{}, {}]".format(x[0],x[1],x[2]))
                    s.nl = "{} [{}, {}]".format(x[0],x[1],x[2])
                    if options.debug:
                        print("==",s.nl)

                elif i == 1:
                    if line == "":
                        i+=0
                    else:
                        #n_us = re.sub('<[^>]*>', '', line).strip()
                        n_us = line
                        s.nus = "; ".join([x.title() for x in n_us.split(",")])

                elif i == 5:
                    #print("SY: {}".format(line))
                    s.syn = line

                elif i == 6:
                   #print("DS:")
                    #print("\n".join(["- {}".format(x) for x in line.split(". ")]))
                    s.ds = "\n".join(["- {}".format(x) for x in line.split(". ")])
                    if options.debug:
                        print("Description:\n{}".format(s.ds))

                elif i == 10:
                    if options.debug:
                        print(line)
                    fl,temp = line.split(".",1)
                    hb,hg,temp = temp.split(";",2)
                    if re.match("\s*introduced",temp):
                        zo,temp = temp.split(";",1)
                    else:
                        zo = temp
                    s.fl = fl.split()[1].strip()
                    s.hb = hb.strip()
                    s.hg = hg.strip()
                    s.zo = zo.strip()
                    s.zg = temp.strip()
                    
                elif i > 10:
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
    url = "http://www.efloras.org/florataxon.aspx?flora_id=1&taxon_id={}".format(id)
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

#url = "http://www.tela-botanica.org/bdtfx-nn-{}-synthese".format(sys.argv[-1])
#url = "http://www.tela-botanica.org/eflore/consultation/service.php?referentiel=bdtfx&niveau=2&module=fiche&action=onglet&num_nom={}&type_nom=&nom=&onglet=description".format(sys.argv[-1])

options = OPTIONS()

tela_ids = sys.argv[1:]
print(tela_ids)
for id in tela_ids:    
    class s:
        hb=""
        zo=""
        ds=""
        fl=""
        fr=""
        nv=""
        nus=""
        syn=""
        id_coste = ""
        n_coste = ""
        syn = []
        oi = []


#    read_file(s,sys.argv[-1])

    read_url(s,id,options)
#    read_url(s,id,"description")
#    read_url(s,id,"nomenclature")

    name = "{}.fona".format(id)
    sys.stderr.write(color.scol("Writting \"{}\" ...\n".format(name),color.YELLOW))
    f = open(name,"w")
    
    f.write("NL: {}\n".format(s.nl))
    f.write("N.US: {}\n".format(s.nus))
    f.write("SY: {}\n".format(s.syn))
    f.write("ID.fona: {}\n".format(s.id_fona))
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
#    if options.split_coste and s.id_coste != "":
#        f.close()
#        print("-"*100)
#        f = open(name_coste)
#        for line in f.readlines():
#            print(color.scol(line,color.GREEN),end="")
        
    print("-"*100)



