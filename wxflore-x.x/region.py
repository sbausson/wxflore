# -*- coding: utf-8 -*-
table = {"Alsace":[u"Alsace",[67,68]],
         "Aquitaine":[u"Aquitaine",[33,40,64,24,47]],
         "Auvergne":[u"Auvergne",[03,15,43,63]],
         "Basse-Normandie":[u"Basse-Normandie",[14,50,61]],
         "Bourgogne":[u"Bourgogne",[21,58,71,89]],
         "Bretagne":[u"Bretagne",[22,29,35,56]],
         "Centre":[u"Centre",[18,28,36,37,41,45]],
         "Champagne-Ardenne":[u"Champagne-Ardenne",[8,10,51,52]],
         "Corse":[u"Corse",[20]],
         "Franche-Comte":[u"Franche-Comté",[25,39,70,90]],
         "Haute-Normandie":[u"Haute-Normandie",[76,27]],
         "IDF":[u"Île-de-France",[75,77,78,91,92,93,94,95]],
         "Languedoc-Roussillon":[u"Languedoc-Roussillon",[11,30,34,48,66]],
         "Limousin":[u"Limousin",[19,23,87]],
         "Lorraine":[u"Lorraine",[54,55,57,88]],
         "Midi-Pyrenees":[u"Midi-Pyrénées",[9,12,31,32,46,65,81,82]],
         "Nord-Pas-de-Calais":[u"Nord-Pas-de-Calais",[59,62]],
         "Pays-de-la-Loire":[u"Pays-de-la-Loire",[44,49,53,72,85]],
         "Picardie":[u"Picardie",[2,60,80]],
         "Poitou-Charentes":[u"Poitou-Charentes",[16,17,79,86]],
         "PACA":[u"Provence-Alpes-Côte-d'Azur",[4,5,6,13,83,84]],
         "Rhone-Alpes":[u"Rhône-Alpes",[1,7,26,38,42,69,73,74]]
}

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def get_region(dep):
    
    for key in table.keys():
        if dep in ['{:02d}'.format(x) for x in table[key][1]]:
            return key

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
