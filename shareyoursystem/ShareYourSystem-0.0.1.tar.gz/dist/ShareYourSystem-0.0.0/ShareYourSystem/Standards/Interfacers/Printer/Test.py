#<ImportSpecificModules>
from ShareYourSystem.Standards.Classors.Representer import _print
from ShareYourSystem.Standards.Interfacers import Printer
#</ImportSpecificModules>

#Print a version of the class
_print(dict(Printer.PrinterClass.__dict__.items()))

#Print a version of this object
_print(Printer.PrinterClass())

#Print a version of his __dict__
_print(Printer.PrinterClass().__dict__)

#Make it print a dict
Printer.PrinterClass()._print({'ParentDict':{'ChildDict':{'MyInt':0},'MyStr':"hello"}})



