#!/usr/bin/env python3

import codecs
import sys
import re
import color

class OPTIONS:
    split_coste = 1


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def bota_name(s):

    #print(s)
    #m = re.match("(\×? ?[A-Z][a-z\.\-\× ]*)([A-Z\(][a-zA-Z,\.\&\-éèàö\) ]*)?\[?([0-9]*).*",s,re.UNICODE)
    m = re.match("(\×? ?[A-Z][a-z\.\-\× ]*)([A-Z\'\(][^\[]*)?\[?([0-9]*).*",s,re.UNICODE)
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
def parse_tela(s,html):
    #f = codecs.open(sys.argv[-1],'r','utf-8')
    #f = open(filename, encoding='ISO-8859-1')
    
    in_coste_desc = 0
    in_fam = 0
    in_nom = 0
    in_ds = 0
    in_desc_col = 0
    in_hb = 0
    in_zo = 0
    in_fl = 0
    in_fr = 0
    in_us = 0
    in_nomenclature = 0
    name_found = 0
    coste_s = ""
    temp_s = ""
    
    for line in html.split("\n"): #f.readlines():
        line = line.strip()
        
        if re.match("""<table class="desc">""",line):
            in_coste_desc = 1
            
        elif in_coste_desc:
            if re.match("</table>",line):
                in_coste_desc = 0

            elif in_ds:
                if re.match("</td>",line):
                    in_ds = 0
                    ss = re.sub('<[^>]*>', '', temp_s.replace("</br>","\n"))
                    s.ds=""
                    for x in ss.split("\n"):
                        s.ds+="{}\n".format(re.sub("^\s*\-\s*\.?\s*","- ",x).strip())
                    s.ds = s.ds.strip()
                else:                    
                    temp_s+=" "+line
                                    
            elif in_hb:
                s.hb = re.sub('<[^>]*>', '', line).strip()
                in_hb = 0

            elif in_zo:
                s.zo = re.sub('<[^>]*>', '', line).strip()
                in_zo = 0

            elif in_fl == 1:
                print("="*50)
                #s.fl = re.sub('<[^>]*>', '', line).replace("Fructification","").strip()
                #s.fl = line.split("<")[0].replace(".","").strip() #re.sub('<[^>]*>', '', line).replace("Fructification","").strip()
                s.fl = re.sub('<[^>]*>', '', line).replace(".","")
                in_fl = -1

                m = re.match(""".*<span class="titre">Fructification (.*)""",line)
                if m:
                    in_fr = 1

            elif in_fr:
                s.fr = re.sub('<[^>]*>', '', line).strip()
                in_fr = 0

            elif in_us:
                s.us = re.sub('<[^>]*>', '', line).strip()
                in_us = 0

            else:
#                coste_s = coste_s.replace('</td></tr>',"")
#                coste_s = coste_s.replace('</span>',"")
#                coste_s = coste_s.replace('<span class="gras">',"")
#                coste_s_ = coste_s.split("<tr><td>")

                #for l in coste_s_:
                m = re.match("""<span class="titre">Écologie (.*)""",line)
                if m:
                    in_hb = 1
                    
                m = re.match("""<span class="titre">Répartition (.*)""",line)
                if m:
                    in_zo = 1
                
                m = re.match("""<span class="titre">Floraison """,line)
                if m and in_fl != -1:
                    in_fl = 1                    

                m = re.match("""<span class="titre">Usages""",line)
                if m:
                    in_us = 1                    

                m = re.match("""([1-9][0-9]*)\s+([A-Z][^<]*)""",line)
                if m:
                    s.id_coste = m.group(1)
                    s.n_coste = m.group(2).strip()
                    
                if re.match("\-",line):
                    in_ds = 1
                    temp_s = line.replace("  "," ")
                        
                #temp_ = coste_s_[1].strip().split(None,1)
                #print("ID.coste: {}".format(temp_[0]))
                #print("N.coste: {}".format(temp_[1]))
                #print("DS:")
                #for l in coste_s_[2].split("</br>"):
                #    print(l.strip().replace("  "," "))
                #
                #hb = coste_s_[3].replace('<span class="titre">Écologie','').strip()
                #print("HB: {}".format(hb))
                #
                #zo = coste_s_[4].replace('<span class="titre">Répartition','').strip()
                #print("ZO: {}".format(zo))
                #
                #fl = coste_s_[5].replace('<span class="titre">Floraison','').strip()
                #print("FL: {}".format(fl))
    
#            else:
#                coste_s += line


        elif re.match('<div class="description wikini editable_sur_clic" title="description">',line):
        #elif re.match("<h2> Description collaborative : </h2>",line):
        #elif re.match("<h4>Description collaborative</h4>",line):
            in_desc_col = 1
            #print("in_desc_col")
            
        elif in_desc_col:
            if re.match("</div>",line):
                in_desc_col = 0
            elif re.match("Participez ",line):
                in_desc_col = 0
                s.ds_col = ""
            else:
                l = re.sub('<[^>]*>', '', line)
                l = l.replace("&gt;",">")
                s.ds_col+="{}\n".format(l.strip())
                
        elif re.match('<span class="famille nomenclature"',line):
            in_fam = 1

        elif 0 and re.match("""<span class="nomenclature""",line):
            in_nomenclature = 1
            
        elif re.match("""<span class="sci">""",line):
            if not name_found:
                name = re.sub('<[^>]*>', '', line).strip()
                #print(name)
                #print(bota_name(name))
                s.nl = bota_name(name)
            name_found = 1
            
        elif re.match("""<span class="nom">""",line):
            in_nom = 1
            
        elif re.match("""Basionyme : <span class="sci">""",line):
            line = line.split(":")[1].strip()
            name = re.sub('<[^>]*>', '', line).strip()
            s.syn.append(bota_name(name))
            
        elif in_nom:
            name = re.sub('<[^>]*>', '', line).strip()
            #print(name)
            #print(bota_name(name))
            n = bota_name(name)
            if n != None:
                s.syn.append(n)
            in_nom = 0
            
        elif in_fam:
            s.fa = re.sub('<[^>]*>', '', line).strip()
            in_fam = 0
            
        elif 0 and in_nomenclature:
            in_nomenclature+=1
            if in_nomenclature == 3:
                s.nl = [re.sub('<[^>]*>', '', line)]
            if in_nomenclature == 4:
                print(line)
                s.nl.append("[{}]".format(re.sub('<[^>]*>', '', line)))
                in_nomenclature = 0

        elif 0 and re.match("""<div class="nom retenu surlignage">""",line):
            in_nom = 1

        elif 0 and in_nom:
            n = re.sub('<[^>]*>', '', line)
            n = n.split("[")[0].strip()
            s.nl = n
            
        else:
            m = re.match("""<div class="conteneur_permalien">Numéro INPN : ([0-9]+)""",line)
            if m:
                s.id_inpn = m.group(1)
                #print(s.id_inpn)
    
            m = re.match("""<div class="conteneur_permalien">Numéro nomenclatural du nom retenu : ([1-9][0-9]*)""",line)
            if m:
                s.id_tela = m.group(1)
                
            m = re.match("""<a id="permalien_wikipedia"  class="lien_externe" href="(.*)" """,line)
            if m:
                s.ref_wiki_fr = m.group(1)
    
            m = re.match("""<h2 class="vernaculaire">(.*)</h2>""",line)
            if m:
                s.nv= m.group(1)

            
#            m = re.match("""<a class="lien_recherche_hier" .*\&fam=(.*)">""",line)
#            if m:
#                s.fa= m.group(1)
    
                
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def read_url(s,id,content):
#    import urllib.request
#    response = urllib.request.urlopen('http://python.org/')
#    html = response.read()


    url = "http://www.tela-botanica.org/bdtfx-nn-{}-{}".format(id,content)
    sys.stderr.write("{}\n".format(url))
    
    values = {}
    
    if 1:
        import urllib
        import urllib.parse
        import urllib.request

        #from http.cookiejar import CookieJar
        import http.cookiejar
        
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        request = urllib.request.Request(url)
        response = opener.open(request)

        page = response.read()
        html = page.decode("iso-8859-1")

#        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
#        headers = { 'User-Agent' : user_agent }
#        
#        req = urllib.request.Request(url,None,headers)
#        response = urllib.request.urlopen(req)
#        page = response.read()
#        html = page.decode("iso-8859-1")

    else:
        import subprocess, os
        cmd = "wget \"{}\"".format(url)
        p = subprocess.Popen(cmd, shell=True)
        html = os.waitpid(p.pid, 0)[1]
        print(html)


        #print(html)
    parse_tela(s,html)
    
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
        ds_col = ""
        fl=""
        fr=""
        nv=""
        us=""
        id_coste = ""
        n_coste = ""
        syn = []

    read_url(s,id,"synthese")
    read_url(s,id,"description")
    read_url(s,id,"nomenclature")

    name = s.nl.replace("× ","").strip()
    name = name.split("[")[0].strip()
    name = name.replace(" subsp. ","-")
    name = name.replace(" f. ","-")
    name = name.replace(" var. ","-")
    name = name.replace(" ",".")
    sys.stderr.write(color.scol("Writting \"{}\" ...\n".format(name),color.YELLOW))
    #f = open(name,"w")
    f = codecs.open(name, 'bw', 'utf-8')

    f.write("FA: {}\n".format(s.fa))
    f.write("NL: {}\n".format(s.nl))
    f.write("NV: {}\n".format(s.nv))
    f.write("SY:\n")
    for syn in s.syn:
        f.write("    {}\n".format(syn))
    f.write("ID.tela: {}\n".format(s.id_tela))

    try:
        f.write("ID.inpn: {}\n".format(s.id_inpn))
    except:
        pass

    f.write("REF.wiki.fr: {}\n".format(s.ref_wiki_fr))
    f.write("ID.coste: {}\n".format(s.id_coste))

    if options.split_coste and s.id_coste != "":
        f.close()
        name_coste = "{}.coste".format(s.id_coste)
        sys.stderr.write(color.scol("Writting \"{}\" ...\n".format(name_coste),color.YELLOW))
        #f = open("{}".format(name_coste),"w")
        f = codecs.open("{}".format(name_coste), 'bw', 'utf-8')

        f.write("ID.coste: {}\n".format(s.id_coste))

        s_res = ""
        s_res+= "N.coste: {}\n".format(s.n_coste)

        if s.ds != "":
            s_res+="DS:\n{}\n".format(s.ds)
        s_res+="HB: {}\n".format(s.hb)
        s_res+="ZO: {}\n".format(s.zo)
        s_res+="FL: {}\n".format(s.fl)
        #print("////",s.fl)
        if s.fr != "":
            s_res+="FR: {}\n".format(s.fr)
        if s.us != "":
            s_res+="US: {}\n".format(s.us)

        #print(s_res)
        f.write(s_res)
        f.close()
        
    if s.ds_col != "":
        name_telacol = "{}.tc".format(name.replace(".","_"))
        sys.stderr.write(color.scol("Writting \"{}\" ...\n".format(name_telacol),color.YELLOW))
        f = open("{}".format(name_telacol),"w")
        f.write(s.ds_col)
        f.close()
            
    print("-"*50)
    f = open(name)
    for line in f.readlines():
        print(line,end="")
        f.close()

    if options.split_coste and s.id_coste != "":
        print("-"*100)
        f = open(name_coste)
        for line in f.readlines():
            print(color.scol(line,color.GREEN),end="")
        f.close()

    if s.ds_col != "":
        print("-"*100)
        f = open(name_telacol)
        for line in f.readlines():
            print(color.scol(line,color.CYAN),end="")
        f.close()

        
    print("-"*100)



