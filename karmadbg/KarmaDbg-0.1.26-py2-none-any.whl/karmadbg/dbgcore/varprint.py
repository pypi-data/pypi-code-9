import pykd
import re
import pkgutil

def getLocals():

    try:
        locals = pykd.getFrame().getParams() + pykd.getFrame().getLocals()
        return [ name  for name, value in locals ]

    except pykd.DbgException:
        return []


def getLocal(localName):

    try:
        locals = dict( pykd.getFrame().getParams() + pykd.getFrame().getLocals() )
        
        subNames = localName.split('.')
        localVar = locals[subNames[0]]
        for subName in subNames[1:]:
            localVar = getMultilinePrinter(localVar).getSubVar(subName)

        return ( subNames[-1], localVar.type().name(), localVar.getAddress(), getShortPrinter(localVar), getMultilinePrinter(localVar).getLines() )

    except pykd.DbgException as e:

        return None


def getTypedVar(varName):
    try:
       
        subNames = varName.split('.')
        var =pykd.typedVar(subNames[0])
        for subName in subNames[1:]:
            var = getMultilinePrinter(var).getSubVar(subName)

        return ( subNames[-1], var.type().name(), var.getAddress(), getShortPrinter(var), getMultilinePrinter(var).getLines() )

    except pykd.DbgException as e:

        return None


def getShortPrinter(var):

    for shortPrinter in shortPrinterList:

        if re.match( shortPrinter[0], var.type().name() ):
            retVal = shortPrinter[1](var)
            if retVal != None:
                return retVal
        
    if var.type().isBase():
        return baseVarPrinter(var)

    if var.type().isPointer():
        return pointerVarPrinter(var)

    if var.type().isArray():
        return "Array"

    if var.type().isUserDefined():
        return "Struct"

    return defaultShortPrinter(var)

def getMultilinePrinter(var):
    
    if var.type().isUserDefined():
        return structMultilinePrinter(var)

    if var.type().isPointer() and var.type().deref().isUserDefined():
        return structMultilinePrinter(var.deref())

    if var.type().isArray():
         return arrayMultilinePrinter(var)

    return defaultMultilinePrinter(var)


def defaultShortPrinter(var):
    return var.type().name()

class defaultMultilinePrinter:

   def __init__(self, var):
       pass

   def getLines(self):
       return []


def baseVarPrinter(var):
    try:
        if var.isInteger():
            return str(long(var))
        else:
            return str(float(var))
    except pykd.MemoryException:
        return "access violation"

def pointerVarPrinter(var):
    if pykd.isValid(var):
        return hex(var)
    else:
        return "invalid memory (0x%x)" % var

class structMultilinePrinter:

    def __init__(self, var):
        self.var = var

    def getLines(self):
       return [ (fieldName, fieldValue.type().name(), fieldValue.getAddress(), getShortPrinter(fieldValue) )  for fieldName, fieldOffset, fieldValue in self.var.fields() ]

    def getSubVar(self, subName):
        return self.var.field(subName)

class arrayMultilinePrinter:

    def __init__(self, var):
        self.var = var

    def getLines(self):
        lst = []
        for i in xrange(min(0x100,len(self.var))):
            val = self.var[i]
            lst.append( ( "[%d]" % (i), val.type().name(), val.getAddress(),  getShortPrinter(val) ) )
        return lst

    def getSubVar(self, subName):

        arrayElem = int(subName[1:-1])
        return self.var[arrayElem]

shortPrinterList = []

def shortprinter(*typeNames):
    
    def decorator(fn):

        for typeName in typeNames:
            shortPrinterList.append( (typeName,fn,) )

        def wrapper(var):

            return fn(var)

        return wrapper

    return decorator

def registerShortPrinters():
    
    import karmadbg.varprinters

    for loader, module_name, ispkg in pkgutil.iter_modules( karmadbg.varprinters.__path__):
        if not ispkg:
            loader.find_module(module_name).load_module(module_name)
 
registerShortPrinters()





















