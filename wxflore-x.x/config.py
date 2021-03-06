import os
import sys

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def read(options):

    class lang:
        show = []
        hide = []

    options.paths.meta = ""
    options.paths.img = ""
    options.paths.snd = ""
    options.lang = lang()

    # Standard config
    if options.config == "" and os.path.exists(os.path.join(options.wxflore,"config")):
        options.config = os.path.join(options.wxflore,"config")

    if not options.noconfig and options.config != "":
        print("Loading config file \"{}\" ...".format(options.config))
        with open(options.config,"r") as f:
            for line in f.readlines():
                line = line.split("#")[0].strip()
                if line != "":
                    name,value= [x.strip() for x in line.split("=")]
                    if name in ["path.root","path.img","path.snd","path.meta","path.bk"]:
                        name = name.split(".")[1]
                        exec("options.paths.{}=value".format(name,value))

                    elif name == "options.lang.show":
                        options.lang.show = value.split(',')

                    elif name == "options.lang.hide":
                        options.lang.hide = value.split(',')

    # No config file
    else:
        script_path = os.path.abspath(os.path.dirname(__file__.decode(sys.stdout.encoding)))
        options.paths.root = os.path.join(os.path.split(script_path)[0],"Flores","Main")
        options.paths.img = os.path.join(options.paths.root,"img")
        options.paths.snd = os.path.join(options.paths.root,"snd")

    print(options.paths.root)
    print(options.paths.img)
    print(options.paths.snd)
    print(options.paths.meta)
    print(options.lang.show)
    print(options.lang.hide)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
