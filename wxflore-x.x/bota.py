#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def ReduceName(name):

    s =  name.split("[")[0]
    s = s.replace("subsp. ","").strip()
    s = s.replace("var. ","").strip()
    s = s.replace(" ","_").replace("'","")
    return s

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def ShortName(name):

    #s = name.replace("["," ").replace("]","")
    s = name.split("[")[0].strip()
    return s

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
