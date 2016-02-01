#!/usr/bin/env python3
# -*- coding: utf-8 -*-

divisions=[
    ["Anseriformes",["Anatidae",
    ]],

    ["Apodiformes",["Apodidae",
    ]],

    ["Charadriiformes",["Alcidae",
                        "Burhinidae",
                        "Charadriidae",
                        "Glareolidae",
                        "Haematopodidae",
                        "Laridae",
                        "Pteroclididae",
                        "Recurvirostridae",
                        "Scolopacidae",
                        "Stercorariidae",
                        "Sternidae",
    ]],

    ["Ciconiiformes",["Ardeidae",
                      "Ciconiidae",
                      "Fregatidae",
                      "Pelecanidae",
                      "Phalacrocoracidae",
                      "Phoenicopteridae",
                      "Sulidae",
                      "Threskiornithidae",
    ]],

    ["Columbiformes",["Columbidae",
    ]],

    ["Coraciiformes",["Alcedinidae",
                      "Coraciidae",
                      "Meropidae",
    ]],

    ["Cuculiformes",["Cuculidae",
    ]],

    ["Falconiformes",["Accipitridae",
                      "Falconidae",
    ]],

    ["Galliformes",["Meleagrididae",
                    "Numididae",
                    "Odontophoridae",
                    "Phasianidae",
    ]],

    ["Gaviiformes",["Gaviidae",
    ]],

    ["Gruiformes",["Gruidae",
                   "Otididae",
                   "Rallidae",
    ]],

    ["Passeriformes",["Aegithalidae",
                      "Alaudidae",
                      "Bombycillidae",
                      "Cardinalidae",
                      "Certhiidae",
                      "Cinclidae",
                      "Cisticolidae",
                      "Corvidae",
                      "Emberizidae",
                      "Estrildidae",
                      "Fringillidae",
                      "Hirundinidae",
                      "Icteridae",
                      "Laniidae",
                      "Leiothrichidae",
                      "Motacillidae",
                      "Muscicapidae",
                      "Oriolidae",
                      "Paridae",
                      "Parulidae",
                      "Passeridae",
                      "Ploceidae",
                      "Prunellidae",
                      "Regulidae",
                      "Remizidae",
                      "Saxicolidae",
                      "Sittidae",
                      "Sturnidae",
                      "Sylviidae",
                      "Tichodromadidae",
                      "Troglodytidae",
                      "Turdidae",
                      "Vireonidae",
    ]],

    ["Piciformes",["Picidae",
    ]],

    ["Podicipediformes",["Podicipedidae",
    ]],

    ["Procellariiformes",["Diomedeidae",
                          "Hydrobatidae",
                          "Procellariidae",
    ]],

    ["Psittaciformes",["Psittacidae",
    ]],

    ["Strigiformes",["Caprimulgidae",
                     "Strigidae",
                     "Tytonidae",
    ]],

    ["Upupiformes",["Upupidae",
    ]],
]

#type_ligneux = ["sous-arbrisseau","arbuste","arbrisseau","petit arbre","arbre","grand arbre","liane","other"]
title = "Oiseaux"
default_division = "Passeriformes"


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    print(sum([div[1] for div in divisions],[]))
