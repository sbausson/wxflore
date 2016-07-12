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

    #-------------------------------------------------------------------------------
    def get(self):
        pass

    #-------------------------------------------------------------------------------
    def handle(self,key_table):

        if self.caract != "":
            caract = self.caract.strip().replace("\n"," ")
            print(caract)
            splited_caract = re.findall(u"([0-9a-c]+’?) – (.*) \.+ (.*)",caract)[0]
            if len(splited_caract) != 3:
                error()
            else:
                print(splited_caract)
                self.ref = splited_caract[0]

            colprint(u"\t| {}".format(caract.strip().replace("\n"," ")),"green")
            colprint(u"\t| {}".format(self.choro.strip().replace("\n"," ")),"yellow")
            colprint(u"\t| {}".format(self.note.strip().replace("\n"," ")),"blue")

            Bitem = {"caract":splited_caract[1],
                     "action":splited_caract[2],
                     "choro":self.choro.replace("\n"," "),
                     "note":self.note}

            key_table[self.ref] = Bitem

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class FloraGallicaKey():

    #-------------------------------------------------------------------------------
    def __init__(self,filename):

        section_type = ""
        header_flag = 1
        self.header = []
        self.key_table = {}

        item = FGBotKeyItem()
        with open(filename,"r") as f:
            for line in f.readlines():
                line = line.decode("utf-8")
                #print("_ _ _",line.strip())
                sys.stdout.write("_ _ _ "+line.strip()+"\n")

                if re.match("^#",line):
                    pass

                elif re.match(u"[1-9a-c][0-9]*’? – ",line):
                    header_flag = 0
                    item.handle(self.key_table)
                    section_type = "caract"
                    item = FGBotKeyItem()
                    item.caract = line

                elif header_flag:
                    print("toto")
                    self.header.append(line)

                elif re.match("[0-9]+\. ",line):
                    section_type = "note"
                    item.note = line.strip()

                elif re.match("^[0-9]+$",line.strip()):
                    pass

                elif re.match(u"Th — |G à drageons — |G à tubercules? — |G à rhizome — |Hydr Th / Hydr Hc —|Hc — |Th/Hc — |Hc/Ch — ",line):
                    section_type = "choro"
                    item.choro = line

                elif re.match(u"Note – ",line):
                    section_type = "note"
                    item.note = line.split(u" – ",1)[1].strip()

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

            item.handle(self.key_table)

        print()


    #-------------------------------------------------------------------------------
    def walk(self,root,level):

        table = []
        for key in [root, root+u'’']:
            item = self.key_table[key]
            #print(level)

            item["key"] = key
            table.append(item)
            if re.match("[1-9]",item["action"]):
                print(indent(level,u"[{}] - {}".format(key,item["caract"])))

                subtable = self.walk(item["action"],level+1)
                table += subtable
            else:
                print(indent(level,u"[{}] - {}".format(key,item["caract"])))

                #first = 1
                #for subcaract in item["caract"].split(";"):
                #    #print(indent(level,"{} - {}".format(key,subcaract)))
                #    if first :
                #        print(indent(level,u"[{}]".format(key)))
                #        first = 0
                #    print(indent(level,u"  - {}".format(subcaract.strip())))

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
        bk = FGK.walk("1",0)
        bkh = FGK.header

        #wxgrid.bkPanel(self,self,bkh,bk,options)
        fgPanel.bkPanel(self,self,bkh,bk,options)
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
