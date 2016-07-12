#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import re
import wx
if __name__ == '__main__':
    sys.path.append("/home/git/wxflore/wxflore-x.x")
import fgPanel

class OPTIONS:
    pass

choro_ids = [u"Th",
             u"G à drageons",
             u"G à tubercules?",
             u"G à rhizome",
             u"Hydr Hc",
             u"Hydr Th",
             u"Hydr Hc",
             u"Hydr Th / Hydr Hc",
             u"Hc",
             u"Th/Hc",
             u"Hc/Ch"]

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def colprint(s,color):

    color_t = {
        "red":91,
        "green":92,
        "yellow":93,
        "blue":94,
        "magenta":95,
        "cyan":96,
        "white":98,
    }

    print(u"\033[{}m{}\033[{}m".format(color_t[color],s,0))

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def indent(level,s):

    return "    "*level + s

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
#class BotKeyItem:
#
#    ref = ""
#    caract = ""
#    choro = ""
#    note = ""
#
#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class FGBotKeyItem():

    #-------------------------------------------------------------------------------
    def __init__(self):
        self.caract = ""
        self.choro = ""
        self.note = ""
        self.group = "main"

    #-------------------------------------------------------------------------------
    def get(self):
        pass

    #-------------------------------------------------------------------------------
    def handle(self,ref,group_t):

        if self.caract != "":
            caract = self.caract.strip().replace("\n"," ")
            #print(caract)

            if re.match(u"([1-9][0-9]*’?) – (.*) \.+ (.*)",caract):
                splited_caract = re.findall(u"([0-9]+’?) – (.*) \.+ (.*)",caract)[0]
            elif re.match(u"([a-z]’?) – (.*) \.+ (.*)",caract):
                splited_caract = re.findall(u"([a-z]’?) – (.*) \.+ (.*)",caract)[0]

            if len(splited_caract) != 3:
                error()
            else:
                print(splited_caract)
                #self.ref = splited_caract[0]

            colprint(u"\t| {}".format(caract.strip().replace("\n"," ")),"green")
            colprint(u"\t| {}".format(self.choro.strip().replace("\n"," ")),"yellow")
            colprint(u"\t| {}".format(self.note.strip().replace("\n"," ")),"blue")

            Bitem = {"ref":splited_caract[0],
                     "caract":splited_caract[1],
                     "action":splited_caract[2],
                     "choro":self.choro.replace("\n"," "),
                     "note":self.note}

            #print("o",ref,group_t[0])
            if not ref in group_t[2]:
                group_t[2][ref] = []

            #print("#####",ref,Bitem["caract"],Bitem["action"])
            group_t[2][ref].append(Bitem)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class FloraGallicaKey():

    #-------------------------------------------------------------------------------
    def __init__(self,filename):

        section_type = ""
        header_flag = 1
        self.groups = [["main",[],{}]]
        self.nref = ""
        group_index = 0

        #self.header = []
        #self.key_table = {}

        item = FGBotKeyItem()
        with open(filename,"r") as f:
            for line in f.readlines():
                line = line.decode("utf-8")
                #print("_ _ _",line.strip())
                sys.stdout.write("_ _ _ "+line.strip()+"\n")

                if re.match("^#",line):
                    pass

                elif re.match(u"[1-9][0-9]*’? – ",line):
                    header_flag = 0
                    item.handle(self.nref,self.groups[group_index])
                    self.nref = re.findall(u"([0-9]+’?) –",line)[0]
                    section_type = "caract"
                    item = FGBotKeyItem()
                    item.caract = line

                elif re.match(u"[a-z]’? – ",line):
                    header_flag = 0
                    item.handle(self.nref,self.groups[group_index])
                    section_type = "caract"
                    item = FGBotKeyItem()
                    item.caract = line

                elif header_flag:
                    self.groups[group_index][1].append(line)

                elif re.match("[1-9][0-9]*\. ",line):
                    section_type = "note"
                    item.note = line.strip()

                elif re.match("^[0-9]+$",line.strip()):
                    pass

                #elif re.match(u"Th — |G à drageons — |G à tubercules? — |G à rhizome — |Hydr Hc — |Hydr Th / Hydr Hc —|Hc — |Th/Hc — |Hc/Ch — ",line):
                elif re.match("|".join([x + u" — " for x in choro_ids]),line,re.U):
                    section_type = "choro"
                    item.choro = line

                elif re.match(u"Note – ",line):
                    section_type = "note"
                    item.note = line.split(u" – ",1)[1].strip()

                elif re.match(u"Groupe [A-Z]",line):
                    item.handle(self.nref,self.groups[group_index])
                    item.group = re.findall(u"(Groupe [A-Z])",line)[0]
                    header_flag = 1
                    group_index+=1
                    self.groups.append([item.group,[line],{}])

                else:
                    if section_type == "caract":
                        item.caract += line
                        #print(".... append key")
                    elif section_type == "choro":
                        item.choro += line
                        #print(".... append choro")
                    elif section_type == "note":
                        item.note += line.strip()
                        #print(".... append note")
                    else:
                        print("??????",line)

            #item.handle(self.key_table)
            item.handle(self.nref,self.groups[group_index])

        print()


    #-------------------------------------------------------------------------------
    def walk(self,root,group,level):

        table = []

        for key in [root, root+u'’']:
            #print(group,key,root)
            #print(group)
            #print(key,group[2].keys())
            for item in group[2][key]:

                item["key"] = key
                table.append(item)
                if re.match("([1-9][0-9]*|[a-z]’?)$",item["action"]):
                    print(indent(level,u"[{}] - {}".format(item["ref"],item["caract"])))

                    subtable = self.walk(item["action"],group,level+1)
                    table += subtable
                else:
                    print(indent(level,u"[{}] - {}".format(item["ref"],item["caract"])))

                    colprint(indent(level,u"= {}".format(item["action"])),"yellow")
                    print(indent(level,u"{}".format(item["choro"])))

                    if item["note"] != "":
                        print(indent(level,u"Note: {}".format(item["note"])))
                    print("")

        return table

#-------------------------------------------------------------------------------
def parse_argv(options):

    i = 1
    while i < len(sys.argv):

        if i == (len(sys.argv) - 1):
            options.filename = sys.argv[i]

        i+=1

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class fgFrame(wx.Frame):

    #-------------------------------------------------------------------------------
    def __init__(self,filename):
        wx.Frame.__init__(self, None, size=(1400,1000), title=u" Clé Flora Gallica ({})".format(""))

        options = OPTIONS()
        options.filename=filename
        FGK = FloraGallicaKey(options.filename)

        bk_t = []
        for G in FGK.groups:
            bk = FGK.walk("1",G,0)
            #bkh = FGK.header
            bk_t.append([G[1],bk])


        #wxgrid.bkPanel(self,self,bkh,bk,options)
        fgPanel.bkPanel(self,self,bk_t,options)
        self.Show()

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':

    options = OPTIONS()
    parse_argv(options)

    app = wx.App(redirect=False)
    fgFrame(options.filename)
    app.MainLoop()
