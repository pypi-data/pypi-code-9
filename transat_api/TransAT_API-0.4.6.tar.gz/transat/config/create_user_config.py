import os
import sys

config = """
[wd]
local: simulations

[tmb_path]
local: C:\Program Files\Ascomp\TransATSuite-5.2\\transatMB\\bin

[path]
ui: C:\Program Files\Ascomp\TransATSuite-5.2\\transatUI\\bin
freecad: C:\Program Files (x86)\FreeCAD 0.15\\bin
db: db.json

[paraview]
site-packages : C:\Program Files (x86)\ParaView 4.3.1\lib\paraview-4.3\site-packages
shared : C:\Program Files (x86)\ParaView 4.3.1\\bin
"""



if __name__ == '__main__':
    filename = 'user_config.ini'
    print "Going to create a new file called "+filename
    print "This file has the default parameters for transat-api."
    if os.path.exists(filename):
        print "There is already a file "+filename+". Should I overwrite it? (y/n): "
        answer = raw_input()
        if answer is not "y":
            sys.exit()
    try:
        f = open(filename, 'w')
        f.write(config)

    except:
        print "could not write "+filename
