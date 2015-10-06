import jpype
from _functools import reduce


# Initialisation

def initSimplace (installDir, workDir, outputDir, additionalClasspathList=[], javaParameters=''):
    
    ''' Initialisation of Simplace '''
    
    cplist = [
        "simplace/build/classes",
        "simplace/conf",
        "lap/build/classes",
        "simplacerun/build/classes",
        "simplacerun/conf",
        "simplace/lib/simplace.jar",
        "simplace/lib/simplace_run.jar",
        "simplace/lib/simplace-lap.jar",
        "simplace/lib/schmitzm-core-2.7-SNAPSHOT.jar",
        "simplace/lib/schmitzm-gt-2.7-SNAPSHOT.jar",
        "simplace/lib/hsqldb-1.8.0.7.jar",
        "simplace/lib/schmitzm/schmitzm-core-2.7-SNAPSHOT.jar",
        "simplace/lib/schmitzm/schmitzm-gt-2.7-SNAPSHOT.jar",
        "simplace/lib/geotools/hsqldb-1.8.0.7.jar",
        "simplace/lib/commons-io-1.3.1.jar",
        "simplace/lib/commons-lang-2.4.jar",
        "simplace/lib/h2-1.1.117.jar",
        "simplace/lib/javaws.jar",
        "simplace/lib/jaxen-full.jar",
        "simplace/lib/jdom.jar",
        "simplace/lib/jfreechart-1.0.14.jar",
        "simplace/lib/jcommon-1.0.17.jar",
        "simplace/lib/jRegistryKey.jar",
        "simplace/lib/log4j-1.2.15.jar",
        "simplace/lib/oro.jar",
        "simplace/lib/saxpath.jar",
        "simplace/lib/xercesImpl-2.7.1.jar",
        "simplace/lib/jena-2.6.4.jar",
        "simplace/lib/iri-0.8.jar",
        "simplace/lib/icu4j-3.4.4.jar",
        "simplace/lib/slf4j-api-1.5.11.jar",
        "simplace/lib/slf4j-log4j12-1.5.11.jar",
        "lapclient/lib/ant.jar",
        "lapclient/lib/ant-launcher.jar",
        "lapclient/lib/jtds.jar",
        "lapclient/lib/postgresql.jar",
        "simplace/lib/org.eclipse.mylyn.wikitext.core_2.0.0.20140108-1934.jar",
        "simplace/lib/org.eclipse.mylyn.wikitext.tracwiki.core_2.0.0.20131126-1957.jar",
        "simplace/lib/commons-jexl-2.1.1.jar",
        "simplace/res/files",    
        "simplace/lib/geotools/commons-logging-1.1.1.jar",
        "simplace/lib/jcifs-1.3.17.jar"  
    ]
    
    fullpathcplist = [installDir + s for s in cplist]
    allcplist = fullpathcplist + additionalClasspathList
    cpstring = reduce(lambda a,b : a+';'+b, allcplist)
    cp = '-Djava.class.path='+cpstring
    
    jpype.startJVM(jpype.getDefaultJVMPath(), cp, javaParameters)
    SimplaceWrapper = jpype.JClass('net.simplace.simulation.wrapper.SimplaceWrapper')
    simplace = SimplaceWrapper(workDir,outputDir)
    return simplace


# Open and close Project

def openProject(simplaceInstance,solution, project=None):
    simplaceInstance.prepareSession(project, solution)
        
def closeProject(simplaceInstance):
    simplaceInstance.finalize()        


# Running and configuring projects

def setProjectLines(simplaceInstance, lines):
    if type(lines) is list :
        lines = reduce(lambda a,b : str(a)+','+str(b), lines)
    simplaceInstance.setProjectLines(lines)   

def runProject(simplaceInstance):
    simplaceInstance.run()


# Creating, configuring and running simulations

def createSimulation(simplaceInstance, paramList = None, queue=True):
    par = _parameterListToArray(paramList)
    return simplaceInstance.createSimulation(par)

def getSimulationIDs(simplaceInstance):
    return [si for si in simplaceInstance.getSimulationIDs()]

def setSimulationValues(simplaceInstance, paramList):
    simplaceInstance.setSimulationValues(_parameterListToArray(paramList))

def runSimulations(simplaceInstance, selectsimulation = False):
    simplaceInstance.runSimulations(selectsimulation)

def stepSimulation(simplaceInstance, count=1, paramList=None, resultFilter=None):
    par = _parameterListToArray(paramList)
    return simplaceInstance.step(par,resultFilter,count)


# Fetch results and convert it to python objects
    
def getResult(simplaceInstance, output, simulation):
    return simplaceInstance.getResult(output, simulation)

def resultToList(result, expand = True, start=None, end=None):
    if(start!=None and end!=None and start > end and start > 0) :
        obj =  result.getDataObjects(start, end)
    else :
        obj =  result.getDataObjects()
    names = result.getHeaderStrings()
    types = result.getTypeStrings()
    return {names[i]:_objectArrayToData(obj[i],types[i],expand) for i in range(0,len(names)-1)}

def varmapToList(result, expand = True):
    names = result.getHeaderStrings()
    obj =  result.getDataObjects()
    types = result.getTypeStrings()
    return {names[i]:_objectToData(obj[i],types[i],expand) for i in range(0,len(names)-1)}

def getUnitsOfResult(result):
    names = result.getHeaderStrings()
    units =  result.getHeaderUnits()
    return {names[i]:units[i] for i in range(0,len(names)-1)}


# Configuration

def setSlotCount(count):   
    jpype.JClass('net.simplace.simulation.FWSimEngine').setSlotCount(count)  
        
def setLogLevel(level):
    LOG = jpype.JClass('net.simplace.simulation.io.logging.Logger')
    LOGL = jpype.JClass('net.simplace.simulation.io.logging.Logger$LOGLEVEL')
    LOG.setLogLevel(LOGL.valueOf(level))
    
def setCheckLevel(simplaceInstance, level):
    simplaceInstance.setCheckLevel(level)   


# Helper Functions

def _objectArrayToData(obj, simplaceType, expand = True):
    if (simplaceType in ['DOUBLE','INT','BOOLEAN']):
        return [o for o in jpype.JClass('org.apache.commons.lang.ArrayUtils').toPrimitive(obj)]
    else:
        if expand and simplaceType in ['DOUBLEARRAY','INTARRAY']:
            return [[o for o in jpype.JClass('org.apache.commons.lang.ArrayUtils').toPrimitive(row)] for row in obj]
        else:
            if simplaceType in ['CHAR','DATE']:
                return [o for o in obj]
            else:
                return obj
            
def _objectToData(obj, simplaceType, expand = True):
    if (simplaceType in ['DOUBLE']):
        return obj.doubleValue()
    else:
        if expand and simplaceType in ['DOUBLEARRAY','INTARRAY']:
            return [o for o in jpype.JClass('org.apache.commons.lang.ArrayUtils').toPrimitive(obj)]
        else:
            return obj            
        

def _parameterListToArray(parameter):
    if parameter==None:
        return None
    else:
        return jpype.JArray(jpype.java.lang.Object, 2)([[key, _getScalarOrList(parameter[key])] for key in parameter.keys() ])
    
def _getScalarOrList(obj):
    if type(obj) is list :
        if all(type(a) is int for a in obj) :
            return jpype.JArray(jpype.JInt, 1)(obj)
        else :
            return jpype.JArray(jpype.JDouble, 1)(obj)
    else :
        return obj