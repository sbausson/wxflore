#!/usr/bin/env python3
# -*- coding: utf-8 -*-

divisions=[

    ["Bryophytes",["Marchantiaceae",
                   "Polytrichaceae",
               ]],
    
    ["Pteridophyte",["Aspleniaceae",
                     "Azollaceae",
                     "Blechnaceae",
                     "Cystopteridaceae",
                     "Dennstaedtiaceae",
                     "Dryopteridaceae",
                     "Equisetaceae",
                     "Hymenophyllaceae",
                     "Marsileaceae",
                     "Onocleaceae",
                     "Ophioglossaceae",
                     "Osmundaceae",
                     "Polypodiaceae",
                     "Pteridaceae",
                     "Salviniaceae",                
                     "Thelypteridaceae",
                     "Woodsiaceae",
                     ]],

    ["Lycopods",["Isoetaceae",
                 "Lycopodiaceae",
                 "Selaginellaceae",
                 ]],

    ["Monocots",["Acoraceae",
                 "Alismataceae",
                 "Amaryllidaceae",
                 "Aponogetonaceae",
                 "Araceae",
                 "Asparagaceae",
                 "Bromeliaceae",
                 "Butomaceae",
                 "Colchicaceae",
                 "Commelinaceae",
                 "Cymodoceaceae",
                 "Cyperaceae",
                 "Dioscoreaceae",
                 "Hydrocharitaceae",
                 "Iridaceae",
                 "Juncaceae",
                 "Juncaginaceae",
                 "Liliaceae",
                 "Menyanthaceae",
                 "Musaceae",
                 "Nartheciaceae",
                 "Orchidaceae",
                 "Poaceae",
                 "Posidoniaceae",
                 "Potamogetonaceae",
                 #"Ruscaceae",
                 "Restionaceae",
                 "Ruppiaceae",
                 "Scheuchzeriaceae",
                 "Smilacaceae",
                 "Tofieldiaceae",
                 #"Trilliaceae",
                 "Typhaceae",
                 "Xanthorrhoeaceae",
                 "Zingiberaceae",
                 "Zosteraceae",
             ]],

    ["Dicots",[
        # A
        "Acanthaceae",
        "Achariaceae",                           
        "Adoxaceae",
        "Aizoaceae",
        "Amaranthaceae",
        "Anacardiaceae",
        "Annonaceae",
        "Apiaceae",
        "Apocynaceae",
        "Aquifoliaceae",
        "Araliaceae",
        "Araucariaceae",        
        "Aristolochiaceae",
        "Asteraceae",

        # B
        "Balsaminaceae",
        "Begoniaceae",

        "Berberidaceae",
        "Betulaceae",
        "Bignoniaceae",

        "Boraginaceae",
        "Brassicaceae",
        "Buxaceae",

        # C
        "Cactaceae",
        "Campanulaceae",
        "Cannabaceae",
        "Capparaceae",
        "Caprifoliaceae",
        "Caryophyllaceae",
        "Celastraceae",
        "Cistaceae",
        "Clethraceae",
        "Convolvulaceae",
        "Coriariaceae",
        "Cornaceae",
        "Crassulaceae",
        "Cucurbitaceae",
        "Cytinaceae",
        
        # D
        "Droseraceae",

        # E
        "Elaeagnaceae",
        "Elatinaceae",
        "Ericaceae",
        "Escalloniaceae",
        "Euphorbiaceae",

        #F
        "Fabaceae",
        "Fagaceae",
        "Frankeniaceae",

        # G
        "Gentianaceae",
        "Geraniaceae",
        "Gesneriaceae",
        "Grossulariaceae",

        # H
        "Haloragaceae",
        "Hydrangeaceae",
        "Hypericaceae",

        # J
        "Juglandaceae",

        # L
        "Lamiaceae",
        "Lauraceae",
        "Lardizabalaceae",
        "Lentibulariaceae",
        "Limnanthaceae",
        "Linaceae",
        "Linderniaceae",
        "Loganiaceae",
        "Lythraceae",

        # M
        "Malvaceae",
        "Melanthiaceae",
        "Melastomataceae",
        "Molluginaceae",
        "Moraceae",
        "Myricaceae",
        "Myrtaceae",

        # O
        "Oleaceae",
        "Onagraceae",
        "Orobanchaceae",
        "Oxalidaceae",

        # P
        "Paeoniaceae",
        "Papaveraceae",
        "Passifloraceae",
        "Phytolaccaceae",
        "Plantaginaceae",
        "Platanaceae",
        "Plumbaginaceae",
        "Polemoniaceae",
        "Polygalaceae",                          
        "Polygonaceae",
        "Portulacaceae",
        "Primulaceae",

        # R
        "Ranunculaceae",
        "Resedaceae",
        "Rhamnaceae",
        "Rosaceae",
        "Rubiaceae",
        "Rutaceae",

        # S
        "Salicaceae",
        "Santalaceae",
        "Sapindaceae",          
        "Saxifragaceae",
        "Scrophulariaceae",
        "Simaroubaceae",
        "Solanaceae",
        "Staphyleaceae",
        "Styracaceae",
        
        # #
        "Tamaricaceae",
        "Thymelaeaceae",

        # U
        "Ulmaceae",
        "Urticaceae",

         # V
        "Verbenaceae",
        "Violaceae",
        "Vitaceae",

        #Z
        "Zygophyllaceae",
           ]],

#    ["Magnoliids",[,
#               ]],

    ["Gymnospermes",["Cupressaceae",
                     "Ephedraceae",
                     "Pinaceae",
                     "Taxaceae",
                     ]],
]

type_ligneux = ["sous-arbrisseau","arbuste","arbrisseau","petit arbre","arbre","grand arbre","liane","other"]


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    print(sum([div[1] for div in divisions],[]))
