# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function

"""

By Gabriel S. Gusmão (Gabriel Sabença Gusmão)
May, 2015

    XL2Py version 1.0.0 pre-alpha

    ~~~~

    "An Excel 2 Python I/O Structure reShaping"

    :dcright: (c) 2015 Gabriel S. Gusmão
    :license: MIT, see LICENSE for more details.


"""
from . import *
from .. import __author__, __version__
from ..core import np, re, dc, time
from ..com_handlers.handlers import xlcom
from ..conversion_lib.funcs_lib import Funlib

class Processor(object):

    def __init__(self):
        self.__author__ = __author__
        self.__version__ = __version__
        self.__COM = []
        self.__status__ = False
        self.Funlib = Funlib()
        self.__conversion_reference = self.Funlib.conversion_reference
        self.__conditional_reference = self.Funlib.pycond
        self.pyxldata = {'Workbooks' : []}
        self.pyxlformulas = []
        self.pyxlnodes = {0 : []}
        self.datalevel = 0
        self.bkp = []
        self.buffer = {}
        self.calcstruct = []
        self.intranode = []
        self.circularrefs = []
        self.tracer = 0
        self.hascircularreferences = False
        self.iolib = {'inputsref' : [], 'ofcell' : [], 'algorithm' : {}}
        super(Processor,self).__init__()

    def attach_com_obj(self,xlcom_obj):
        if isinstance(xlcom_obj,xlcom):
            self.__COM = xlcom_obj
            if not self.__COM.__status__:
                raise Exception('xlcom object is not connected to a XL file.')
            else:
                pass
        else:
            raise Exception('xlcom_obj must be of type xlcom.')

    def set_pyxlranges(self,pyxllist,values):
        """ set_pyxlranges
        parameters must have been converted by the internal function listconnect
        or be already shapped in the way references point to internal structure (pyxldata)
        params(2):
            pyxllist as iinteger list/tuple
                lists/tuple of [[Workbook as integer],[Worksheet as integer],[[Row as integer],[Column as integer]]]
                e.g. [[1,2,[[2],[4,6]]]] -> Internal nodal reference WB = 1, WS = 2, Column = 2, Rows = 4 to 6
            values as numeric of the same size of total references in pyxllist
        """
        for i in range(0,len(pyxllist)):
            if not all((np.diff(pyxllist[i][2])+1).flatten() == np.shape(values[i])):
                print('pyxlranges ({}) and values ({}) shapes should be the same.'.format((np.diff(pyxllist[i][2])+1).flatten(),np.shape(values[i])))
                raise Exception
            else:
                pass
        for i in range(0,len(pyxllist)):
            val = values[i].flatten().tolist()
            for r in range(min(pyxllist[i][2][0]),max(pyxllist[i][2][0])+1):
                for c in range(min(pyxllist[i][2][1]),max(pyxllist[i][2][1])+1):
                    self.pyxldata[pyxllist[i][0]][pyxllist[i][1]][r][c] = val[0]
                    val.pop(0)

    def get_pyxlranges(self,pyxllist):
        """ get_pyxlranges
        retrieves stored values from the internal structure (pyxldata)
        if they are not stored, they are retrieved from the XL process and then stored
        params (1): pyxllist as in set_pyxlranges
            e.g. [[1,2,[[2],[4,6]]]] -> Internal nodal reference WB = 1, WS = 1, Column = 2, Rows = 4 to 6
        returns pyxllist corresponding value from pyxldata
        """
        pyxlvalues = []
        flag = False
        for item in pyxllist:
            for r in range(min(item[2][0]),max(item[2][0])+1):
                for c in range(min(item[2][1]),max(item[2][1])+1):
                    try:
                        nWB = [item[0] if type(item[0]) is int else self.pyxldata['Workbooks'].index(item[0])+1][0]
                        nWS = [item[1] if type(item[1]) is int else self.pyxldata[nWB]['Worksheets'].index(item[1])+1][0]
                        pyxlvalues.append(self.pyxldata[nWB][nWS][r][c])
                    except:
                        if not flag:
                            print('Range was not read during PyXL strucutre creation.')
                            print('Values being now attached to the structure...')
                        flag = True
                        pyxlvalues = []
                        pyxllist0 = dc(pyxllist)
                        for xlitem in pyxllist:
                            xlitem = self.processxlbuffer(xlitem)
                            for subitem in xlitem:
                                if subitem != []:
                                    self.processxlitem(subitem)
                                else:
                                    pass
                        return self.get_pyxlranges(pyxllist0)[0], flag
        return np.array(pyxlvalues), flag

    def xlformula2py(self,formulas):
        """ xlformula2py
        params (1): formulas as string or list of strings containing R1C1-type xl formulas
        returns the list of XL formuals converted to Python representation
        """
        pfullfun = re.compile(r'[A-Za-z.]+(?=\()[\s|\d|\w|\W][^\(\)]*[\)]')
        pparams = re.compile(r'(?<=[A-Za-z.]\()[\s|\d|\w|\W][^\(\)]*(?=\))')
        pfunctions = re.compile(r'[A-Za-z.]+(?=\((?<=\()[\s|\d|\w|\W][^\(\)]*(?=\)))')
        pcheck = re.compile(r'[A-Za-z.]+\(')
        pchecknon = re.compile(r'(?<![A-Za-z.])(?=\()[\s|\d|\w|\W][^\(\)]*[?=\)]')
        codecode = [['\,','_@@_'],['\(','_@1_'],['\)','_1@_']]
        if type(formulas) is not list:
            formulas = [formulas]
        for i in range(0,len(formulas)):
            xlformula = formulas[i]
            xlformula = xlformula.replace("'",'')
            # convert functions
            while pcheck.search(xlformula):
                # code non function parenthesis
                while pchecknon.search(xlformula):
                    nonfuns = np.unique(pchecknon.findall(xlformula)).tolist()
                    if type(nonfuns) is str:
                        nonfuns = [nonfuns]
                    for j in range(0,len(nonfuns)):
                        replstr = nonfuns[j]
                        for code in codecode:
                            replstr = re.sub(code[0],code[1],replstr)
                        xlformula = xlformula.replace(nonfuns[j],replstr)
                xluniquefuns = np.unique(pfullfun.findall(xlformula)).tolist()
                for j in range(0,len(xluniquefuns)):
                    # check number of parameters
                    xlparams = pparams.findall(repr(xluniquefuns[j]))[0]
                    xlfunctions = pfunctions.findall(repr(xluniquefuns[j]))[0]
                    xlparams = re.split(',',xlparams)
                    reference = self.__conversion_reference[xlfunctions]
                    replstr = reference['pyFormula'](xlparams)
                    for code in codecode:
                        replstr = re.sub(code[0],code[1],replstr)
                    xlformula = xlformula.replace(xluniquefuns[j],replstr)
            for code in codecode:
                xlformula = re.sub(code[1],str(code[0][1]),xlformula)
            xlformula = re.sub('\^','**',xlformula)
            if xlformula[0] == '=':
                xlformula = xlformula[1:len(xlformula)]
            else:
                pass
            for intnum in np.unique(re.compile('.(?<![0-9\.RC\[\]])[0-9]+(?![0-9RC\.\[\]\!]).').findall(xlformula)):
                xlformula = xlformula.replace(intnum,intnum[0:-1]+'.0'+intnum[len(intnum)-1])
            for cond in np.unique(re.compile(r'[<>=]+').findall(xlformula)).tolist():
                xlformula = re.sub(cond,self.__conditional_reference[cond],xlformula)
            formulas[i] = xlformula
        return formulas

    def link_xlranges(self,noderefs):
        """ inner method link_xlranges
        creates formula refs to pyxldata assgined positions
        this basically takes a R1C1 formula and change its R1C1 reference
        to an evaluable string that points to the pyxldata structure
         e.g. WB, WS, R1C1 -> pyxldata[nWB][nWS][R=1][C=1]
        """
        # p as range grabber
        p = re.compile(r'([\w\s\.]+(?=\]))?.?([\w\s\.]+(?=\!))?.?(R[\d]+C[\d]+[[:R]*[\d]*[C]*[\d]*]?)',re.M)
        pR = re.compile(r'(?<=R)\d+')
        pC = re.compile(r'(?<=C)\d+')
        level = noderefs[0]; node = noderefs[1]
        dependence = dict()
        i = self.pyxlnodes[level][node]['formulaindex']
        formulas = self.pyxlformulas[i]
        formulas = p.findall(formulas)
        formulas = list([eval(fstr) for fstr in set([repr(fval) for fval in formulas])])
        for formula in formulas:
            formula = [formula for formula in formula]
            repform = str()
            if formula[0] != '':
                repform += '['+formula[0]+']'
            else:
                pass
            if formula[1] != '':
                repform += formula[1]+"!"
            else:
                pass
            repform += formula[2]
            # coolect worbook and worksheet names WB/WS and indices nWB/nWS that matches those in pyxl data from formula
            WB = [self.pyxlnodes[level][node]['filename'] if formula[0]=='' else formula[0]][0]
            if WB in self.pyxldata['Workbooks']:
                nWB = self.pyxldata['Workbooks'].index(WB)+1
            else:
                self.pyxldata['Workbooks'].append(WB)
                nWB = len(self.pyxldata)
                self.pyxldata.__setitem__(nWB,{'Worksheets' : []})
                self.buffer.__setitem__(WB,{})
            WS = [self.pyxlnodes[level][node]['sheet'] if formula[1]=='' else formula[1]][0]
            if WS in self.pyxldata[nWB]['Worksheets']:
                nWS = self.pyxldata[nWB]['Worksheets'].index(WS)+1
            else:
                self.pyxldata[nWB]['Worksheets'].append(WS)
                nWS = len(self.pyxldata[nWB])
                self.pyxldata[nWB].__setitem__(nWS, {})
                self.buffer[WB].__setitem__(WS,[])
            # collect rows and columns from formula
            R = [int(pos) for pos in pR.findall(formula[2])]
            C = [int(pos) for pos in pC.findall(formula[2])]
            vdim = np.array(R).ptp()+1
            hdim = np.array(C).ptp()+1
            # define WS, WB, rows and columns on which the formula depends
            if dependence.has_key(nWB):
                if dependence[nWB].has_key(nWS):
                    pass
                else:
                    dependence[nWB].__setitem__(nWS,[])
            else:
                dependence.__setitem__(nWB,{nWS : []})
            checker = False
            for refs in dependence[nWB][nWS]:
                if min(refs[0])<=min(R)<=max(refs[0]) and min(refs[0])<=max(R)<=max(refs[0])\
                and min(refs[1])<=min(C)<=max(refs[1]) and min(refs[1])<=max(C)<=max(refs[1]):
                    checker = True
                else:
                    pass
            if checker == False:
                dependence[nWB][nWS].append([R,C])
            else:
                pass
            # create a evaluable string to build cells, arrays or matrices from pyxldata references
            repstr = "np.reshape([self.pyxldata["+repr(nWB)+"]["+repr(nWS)+"][r][c] for r in range("+repr(min(R))+","+repr(max(R))+"+1) for c in range("+repr(min(C))+","+repr(max(C))+"+1)],["+repr(vdim)+","+repr(hdim)+"])"
            self.pyxlformulas[i] = self.pyxlformulas[i].replace(repform,repstr)
        else:
            pass
        self.pyxlformulas[i] = 'np.nan_to_num('+self.pyxlformulas[i]+').tolist()'
        self.pyxlnodes[level][node]['dependence'] = dependence # store dependences

    def creatxlnode(self,WB,WS,address,formula):
        """ inner method/function) creatxlnode
        if node already exists -> returns False
        if node has not been created -> creates node in pyxlnodes
            converts formula to Python evaluable representation  with xlformula2py and store it in pyxlformulas
            indexes pyxlformulas position onto node
            links R1C1 addresses in formula to evaluable references to pyxldata
            returns True
        params (4):
            WB -> Workbook name as string
            WS -> Worksheet name as string
            address -> R1C1-type address
            formula -> R1C1-type formula
        """
        struct = {'filename': WB, 'sheet' : WS, 'row' : [], 'column' : [], 'dim' : [], 'formulaindex' : [], 'dependence' : dict()}
        struct['row'] = [int(R) for R in re.compile(r'(?<=R)[\d]+',re.M).findall(address)]
        struct['column'] = [int(C) for C in re.compile(r'(?<=C)[\d]+',re.M).findall(address)]
        for level in self.pyxlnodes:
            for datastruct in self.pyxlnodes[level]:
                if datastruct['filename'] == struct['filename'] and datastruct['sheet'] == struct['sheet'] and datastruct['row'] == struct['row'] and datastruct['column'] == struct['column']:
                    return False
                else:
                    pass
        formula = self.xlformula2py(formula)
        self.pyxlformulas.append(formula[0])
        formulaindex = len(self.pyxlformulas)-1
        struct['formulaindex'] = formulaindex
        dim = self.__COM.dim_ranges(address)
        struct['dim'] = [int(dim[0][0]), int(dim[0][1])]
        self.pyxlnodes[self.datalevel].append(struct)
        self.link_xlranges([self.datalevel, len(self.pyxlnodes[self.datalevel])-1])
        return True

    def storedata(self,rangeobj,nWS,nWB):
        """ inner method storedata
        Utilized for deploying XL COM range object values into pyxldata structure,
        references by their related WS and WB numbers.
        params (3):
            rangeobj as XL COM range object
            nWS and nWB as references to Workbook and Worksheet, respectively, as integers
        """
        values = []
        values = rangeobj.Value
        rows = [rangeobj.Cells.Row, rangeobj.Cells.Row+rangeobj.Cells.Rows.Count-1]
        columns = [rangeobj.Cells.Column, rangeobj.Cells.Column+rangeobj.Cells.Columns.Count-1]
        if all([type(values) is not var_type for var_type in [tuple,list]]):
            flag = True
        else:
            flag = False
        for Row in range(rows[0],rows[1]+1):
            for Column in range(columns[0],columns[1]+1):
                if flag:
                    Value = values
                else:
                    Value = values[Row-rows[0]][Column-columns[0]]
                if not(self.pyxldata[nWB][nWS].has_key(Row)):
                    self.pyxldata[nWB][nWS].__setitem__(Row, {Column : [Value if Value != None else 0.0][0]})
                elif not(self.pyxldata[nWB][nWS][Row].has_key(Column)):
                    self.pyxldata[nWB][nWS][Row].__setitem__(Column, [Value if Value != None else 0.0][0])
                else:
                    pass

    def processxlitem(self,item): # item as range
        """ inner method processxlitem
            check and add (if not already in) item into object buffer
            creates node for pyxlnodes if item not yet in buffer (save time)
            ... called by xlstruct_constructor in recursive way in case XL object derived from
            item have dependents (dependents are then processed in tree-branch inner loops)
            params (1):
                item as range reference -> list or tuple of indexed WB, WS, rows and columns
        """
        WB = item[0]
        WS = item[1]
        R = item[2][0]
        C = item[2][1]
        if type(WS) is not int:
            if WB != self.__COM.Workbook.Name or WS != self.__COM.Worksheet.Name: # Change WB and WS if necessary
                self.__COM.change_path(WB,WS)
        else:
            if WS != self.pyxldata[WB]['Worksheets'].index(self.__COM.Worksheet.Name)+1:
                self.__COM.change_path(WB,WS)
        xladdress = [[r,c] for r in range(min(R),max(R)+1) for c in range(min(C),max(C)+1)]
        formula_array = []
        nWB = [WB if type(WB) is int else self.pyxldata['Workbooks'].index(WB)+1][0]
        WB = [self.pyxldata['Workbooks'][nWB-1] if type(WB) is int else WB][0]
        nWS = [WS if type(WS)  is int else self.pyxldata[nWB]['Worksheets'].index(WS)+1][0]
        WS = [self.pyxldata[nWB]['Worksheets'][nWS-1] if type(WS) is int else WS][0]
        if re.search(r'[A-Z][0-9]',repr(self.__COM.get_com_ranges_r1c1(R,C).Formula)):
            hasprecedents = True
        else:
            hasprecedents = False
        if hasprecedents:
            # find precedents
            while len(xladdress)>0:
                rangeobj = self.__COM.get_com_ranges_r1c1([xladdress[0][0]],[xladdress[0][1]])
                if rangeobj.HasArray:
                    xlobj = rangeobj.CurrentArray
                    arrayaddress = self.__COM.convert_r1c1A1(xlobj.Address)[0]
                    r = [int(r) for r in re.compile(r'(?<=R)\d+').findall(arrayaddress)]
                    c = [int(c) for c in re.compile(r'(?<=C)\d+').findall(arrayaddress)]
                    if [r,c] not in self.buffer[WB][WS]:
                        self.buffer[WB][WS].append([r,c])
                    arrayaddress = [r,c]
                else:
                    xlobj = rangeobj
                self.storedata(xlobj,nWS,nWB)
                xladdress.__delitem__(0)
                if xlobj.HasArray and xlobj.Cells.Count>1: # checks for array
                    # process in tree-branch inner loop precedents in object
                    for r in range(arrayaddress[0][0],arrayaddress[0][1]+1):
                        for c in range(arrayaddress[1][0],arrayaddress[1][1]+1):
                            if xladdress.count([r,c]):
                                xladdress.remove([r,c])
                    address = self.__COM.convert_r1c1A1(xlobj.Address)[0]
                    formula = self.__COM.convert_r1c1A1(xlobj.FormulaArray)[0]
                    if formula[0] == '=' and not formula.__contains__('ATG'):
                        # create node and append precedents to be processed
                        if self.creatxlnode(WB,WS,address,formula):
                            formula_array.append([formula,xlobj.Parent.Parent.Name,xlobj.Parent.Name])
                    else:
                        pass
                else:
                    # single precedent (no array)
                    address = self.__COM.convert_r1c1A1(xlobj.Address)[0]
                    formula = self.__COM.convert_r1c1A1(xlobj.Formula)[0]
                    if formula[0] == '=' and not formula.__contains__('ATG'):
                        # create node and append precedents to be processed
                        if self.creatxlnode(WB,WS,address,formula):
                            formula_array.append([formula,xlobj.Parent.Parent.Name,xlobj.Parent.Name])
                    else:
                        pass
            if len(formula_array)>0:
                self.datalevel += 1 # go down one level
                for formula in formula_array:
                    self.xlstruct_constructor(*formula) # loop into precedents
                self.datalevel -= 1 # move back to main level
            else:
                pass
        else:
            self.storedata(self.__COM.get_com_ranges_r1c1(R,C),nWS,nWB)

    def processxlbuffer(self,item):
        """ inner method/function processxlbuffer
            processes new item from xlstruct_constructor into buffer
            if item
                is in buffer -> return []
                overalps buffered item -> return complement of item and buffered item, store complement into buffer
                is not in buffer -> return full item, store full item into buffer
        """
        item = [item]
        WB = item[0][0]; WS = item[0][1];
        nWB = [WB if type(WB) is int else self.pyxldata['Workbooks'].index(WB)+1][0]
        WB = [self.pyxldata['Workbooks'][nWB-1] if type(WB) is int else WB][0]
        nWS = [WS if type(WS)  is int else self.pyxldata[nWB]['Worksheets'].index(WS)+1][0]
        WS = [self.pyxldata[nWB]['Worksheets'][nWS-1] if type(WS) is int else WS][0]
        if WB not in self.buffer:
            self.buffer.__setitem__(WB,{WS:[item[0][2]]})
            self.pyxldata['Workbooks'].append(WB)
            self.pyxldata.__setitem__(len(self.pyxldata),{'Worksheets':[WS]})
            self.pyxldata[len(self.pyxldata['Workbooks'])].__setitem__(1,{})
        elif WS not in self.buffer[WB]:
            self.buffer[WB].__setitem__(WS,[item[0][2]])
            nWB = self.pyxldata['Workbooks'].index(WB)+1
            self.pyxldata[nWB]['Worksheets'].append(WS)
            self.pyxldata[nWB].__setitem__(len(self.pyxldata[nWB]['Worksheets']),{1 : {}})
        else:
            numitem = len(item)-1
            while numitem <= len(item)-1:
                new_item = []
                sub_item = item[numitem]
                buffer0 = [buffered for buffered in self.buffer[WB][WS]]
                while new_item != sub_item and sub_item != []:
                    R = sub_item[2][0]; C = sub_item[2][1]
                    new_item = sub_item
                    while len(buffer0)>0:
                        rc = buffer0[0]
                        if min(R)>=min(rc[0]) and max(R)<=max(rc[0]) and min(C)>=min(rc[1]) and max(C)<=max(rc[1]):
                            sub_item = []
                            item[numitem] = sub_item
                            break
                        elif min(C)>=min(rc[1]) and max(C)<=max(rc[1]): # range withing buffered columns
                            if max(rc[0])>=min(R)>=min(rc[0]) and max(R)>max(rc[0]):
                                R[R.index(min(R))] = max(rc[0])+1
                                buffer0 = buffer0[1:len(buffer0)]+[buffer0[0]]
                            elif min(R)<min(rc[0]) and min(rc[0])<=max(R)<=max(rc[0]):
                                R[R.index(max(R))] = min(rc[0])-1
                                buffer0 = buffer0[1:len(buffer0)]+[buffer0[0]]
                            else:
                                buffer0.remove(rc)
                        elif min(R)>=min(rc[0]) and max(R)<=max(rc[0]): # range withing buffered lines
                            if max(rc[1])>=min(C)>=min(rc[1]) and max(C)>max(rc[1]):
                                C[C.index(min(C))] = max(rc[1])+1
                                buffer0 = buffer0[1:len(buffer0)]+[buffer0[0]]
                            elif min(C)<min(rc[1]) and min(rc[1])<=max(C)<=max(rc[1]):
                                C[C.index(max(C))] = min(rc[1])-1
                                buffer0 = buffer0[1:len(buffer0)]+[buffer0[0]]
                            else:
                                buffer0.remove(rc)
                        # item-breaker conditions below
                        elif max(rc[0])>=max(R)>=min(rc[0]) and max(rc[1])>=max(C)>=min(rc[1]): # range overalap rc first quadrant
                            item.append([WB,WS,[[min(rc[0]),R[R==max(R)]],[C[C==min(C)],min(rc[1])-1]]])
                            R[R.index(max(R))] = min(rc[0])-1
                        elif max(rc[0])>=max(R)>=min(rc[0]) and min(rc[1])<=min(C)<=max(rc[1]): # range overalap rc second quadrant
                            item.append([WB,WS,[[min(rc[0]),R[R==max(R)]],[max(rc[1])+1,C[C==max(C)]]]])
                            R[R.index(max(R))] = min(rc[0])-1
                        elif min(rc[0])<=min(R)<=max(rc[0]) and max(rc[1])>=max(C)>=min(rc[1]): # range overalap rc third quadrant
                            item.append([WB,WS,[[R[R==min(R)],max(rc[0])],[C[C==min(C)],min(rc[1])-1]]])
                            R[R.index(min(R))] = max(rc[0])+1
                        elif min(rc[0])<=min(R)<=max(rc[0]) and min(rc[1])<=min(C)<=max(rc[1]): # range overalap rc foruth quadrant
                            item.append([WB,WS,[[R[R==min(R)],max(rc[0])],[max(rc[1])+1,C[C==max(C)]]]])
                            R[R.index(min(R))] = max(rc[0])+1
                        else:
                            buffer0.remove(rc)
                        sub_item = [WB, WS, [R,C]]
                        item[numitem] = sub_item
                numitem += 1
            for sub_item in item:
                if sub_item != []:
                    self.buffer[WB][WS].append(sub_item[2])
        return item

    def xlstruct_constructor(self,formula,WB0,WS0):
        """ inner method/function (called recursivelly)
        Base function / method for scrapping the XL spreadsheet
            - Extracts R1C1 cell references from formula
            - Checks whether R1C1 references have been processed with processxlbuffer
            - Process items that have not been processed with processxlitem
        """
        if self.pyxlnodes.__contains__(self.datalevel) is False:
            self.pyxlnodes.__setitem__(self.datalevel,[])
        formula = formula.replace("'",'')
        p = re.compile(r'([\w\s\.]+(?=\]))?.?([\w\s\.]+(?=\!))?.?(R[\d]+C[\d]+[[:R]*[\d]*[C]*[\d]*]?)',re.M)
        itemlist = [list(item) for item in p.findall(formula)]
        while len(itemlist) > 0:
            item = []
            for iteritem in itemlist:
                if iteritem[1] == '':
                    iteritem[0] = WB0
                    iteritem[1] = WS0
                    item = iteritem
                    break
                elif iteritem[0] == '':
                    iteritem[0] = WB0
                    item = iteritem
                    break
                elif iteritem[1] == WS0 and iteritem[0] == WB0:
                    item = iteritem
                    break
                else:
                    pass
            if item == []:
                item = iteritem
            else:
                pass
            while itemlist.count(item)>0:
                itemlist.remove(item)
            R = [int(R) for R in re.compile(r'(?<=R)[\d]+',re.M).findall(item[2])]
            C = [int(C) for C in re.compile(r'(?<=C)[\d]+',re.M).findall(item[2])]
            item[2] = [R,C]
            item = self.processxlbuffer(item)
            if len(item) != 0:
                for sub_item in item:
                    if sub_item != []:
                        self.processxlitem(sub_item)        # break the item into those who do and do not belong to arryas
            else:
                pass

    def createpyxlnodes(self,ofcell):
        """ START inner method createpyxlnodes (ofcell as tree root)
            - Sets the pyxldata structure framework
            - Sets the pyxlnodes tree structure root (createxlnode)
            - Calls the recursive method xlstruct_constructor as of the ofcell formula
            ... recursive process begins
        """
        # first derive actual WB-WS-Range from ofcell
        self.__COM.change_path(ofcell[0],ofcell[1])
        if re.compile('R\d+C\d+').search(str(ofcell[2])):
            ofcell[2] = self.__COM.convert_r1c1A1(ofcell[2])
        ofcellobj = self.__COM.Worksheet.Range(ofcell[2])
        print('Converting xl structure to py...')
        t0 = time.time()
        WB = self.__COM.Workbook.Name
        WS = self.__COM.Worksheet.Name
        bkp = self.__COM.change_path(WB,WS)
        formulaof = self.__COM.get_formulas_r1c1(ofcell[2]) # get formula cells/ranges
        # structure and dependences initializations
        self.pyxldata['Workbooks'].append(WB)
        self.pyxldata.__setitem__(1,{'Worksheets' : [WS]})
        self.pyxldata[1].__setitem__(1,{ofcellobj.Cells.Row : {ofcellobj.Cells.Column : ofcellobj.Cells.Value}})
        # preallocate OF cell in buffer
        self.buffer.__setitem__(WB,{WS:[[[ofcellobj.Cells.Row], [ofcellobj.Cells.Column]]]})
        self.creatxlnode(WB,WS,self.__COM.convert_r1c1A1(ofcell[2])[0],self.__COM.convert_r1c1A1(ofcellobj.Formula))
        self.datalevel += 1
        self.xlstruct_constructor(formulaof[0],WB,WS)
        if self.__COM.Workbook.Name != WB or self.__COM.Worksheet.Name != WS:
            self.__COM.change_path([],[],bkp)
        self.__status__ = True
        print('Completed (elapsed time:{}s)'.format(time.time()-t0))

    def findpyxlnodes(self,nWB,nWS,row,column):
        """ findpyxlnodes
        params (4):
            nWB -> Workbook number in pyxldata as integer
            nWS -> Worksheet number in pyxldata[nWB] as integer
            row -> Row number as integer
            column -> Column number as integer
        returns a list of [level, nodes] that entails the parsed reference
        """
        nodes = []
        for level in self.pyxlnodes:
            for node in self.pyxlnodes[level]:
                if node['filename'] == self.pyxldata['Workbooks'][nWB-1]:
                    if node['sheet'] == self.pyxldata[nWB]['Worksheets'][nWS-1]:
                        if min(node['row'])<= row and max(node['row'])>= row:
                            if min(node['column'])<= column and max(node['column'])>= column:
                                nodes.append([level,self.pyxlnodes[level].index(node)])
        return nodes

    def evalpyxlnodes(self,level,node):
        """ method evalpyxlnodes
        Updates the cell/array in  pyxldata to which the node makes reference
        by evaluating their converted formula using eval() and updates
        params(2):
            level as int
            node as int
        """
        value = eval(self.pyxlformulas[self.pyxlnodes[level][node]['formulaindex']])
        if type(value) is not list:
            value = [[value]]
        elif type(value[0]) is not list:
            value = [[value] for value in value]
        else:
            pass
        R = self.pyxlnodes[level][node]['row']
        C = self.pyxlnodes[level][node]['column']
        nWB = self.pyxldata['Workbooks'].index(self.pyxlnodes[level][node]['filename'])+1
        nWS = self.pyxldata[nWB]['Worksheets'].index(self.pyxlnodes[level][node]['sheet'])+1
        for r in range(min(R),max(R)+1):
            for c in range(min(C),max(C)+1):
                self.pyxldata[nWB][nWS][r][c] = float(value[r-min(R)][c-min(C)])

    def validatenodes(self):
        """ validatenodes
            evaluate all nodes and compare the difference between the evaluation results
            and actually pyxldata cell value. If the relative change is greater than 1e-10,
            the createcalcstruct inner method failed to bind node dependencies, returning False
            Otherwise, return True
            """
        flag = True
        print('Starting PyXL structure validation...')
        t0 = time.time()
        for level in self.pyxlnodes:
            for node in range(0,len(self.pyxlnodes[level])):
                value = eval(self.pyxlformulas[self.pyxlnodes[level][node]['formulaindex']])
                if type(value) is not list:
                    value = [[value]]
                elif type(value[0]) is not list:
                    value = [[value] for value in value]
                else:
                    pass
                R = self.pyxlnodes[level][node]['row']
                C = self.pyxlnodes[level][node]['column']
                nWB = self.pyxldata['Workbooks'].index(self.pyxlnodes[level][node]['filename'])+1
                nWS = self.pyxldata[nWB]['Worksheets'].index(self.pyxlnodes[level][node]['sheet'])+1
                for r in range(min(R),max(R)+1):
                    for c in range(min(C),max(C)+1):
                        #print self.pyxldata[nWB][nWS][r][c], value[r-min(R)][c-min(C)]
                        if np.divide(abs(self.pyxldata[nWB][nWS][r][c] - value[r-min(R)][c-min(C)]),self.pyxldata[nWB][nWS][r][c])>1e-10:
                            print('Original:', self.pyxldata[nWB][nWS][r][c], 'Calculated:', value[r-min(R)][c-min(C)])
                            print('Level {} : Node {} failed validations (nWB {}, nWS {}, R{}C{})'.format(level,node,nWB,nWS,r,c))
                            flag = False
        if flag is True:
            print('Validation successfully completed (elapsed time: {}s)'.format(time.time()-t0))
        else:
            print('Validation failed. Check parsed input.')
        return flag

    def circularrefwalker(self,index,index0,nodebuff):
        """ inner recursive method/function circularrefwalker
            recusively walk into all intranodes, hopping onto the next reference
            to see whether it gets to the starting point, thus comprising a circular reference
            circular references pairs are added to circularrefs list
            params(2):
                index as integer
                index0 as integer
                nodebuff as list (updated recursively)
        """
        ref0 = self.intranode[index][1]
        base = self.intranode[index0][0]
        for ref in ref0:
            if ref == base:
                if any([pair in self.circularrefs for pair in [[base, self.intranode[index][0]], [self.intranode[index][0], base]]]):
                    pass
                else:
                    self.circularrefs.append([base,self.intranode[index][0]])
            else:
                vec = [i[0] for i in self.intranode]
                if ref in vec:
                    nxtindex = vec.index(ref)
                    if nxtindex not in nodebuff:
                        nodebuff.append(nxtindex)
                        self.circularrefwalker(nxtindex,index0,nodebuff)
                    else:
                        pass

    def createintranodes(self):
        """ inner method createintranodes
            creates intranode list of dependencies between nodes from node dependencies
        """
        for level in self.pyxlnodes:
            for node in range(0,len(self.pyxlnodes[level])):
                for nWB in self.pyxlnodes[level][node]['dependence']:
                    for nWS in self.pyxlnodes[level][node]['dependence'][nWB]:
                        for item in self.pyxlnodes[level][node]['dependence'][nWB][nWS]:
                            for innerlevel in self.pyxlnodes:
                                for innernode in range(0,len(self.pyxlnodes[innerlevel])):
                                    WB = self.pyxlnodes[innerlevel][innernode]['filename']
                                    WS = self.pyxlnodes[innerlevel][innernode]['sheet']
                                    nWBin = self.pyxldata['Workbooks'].index(WB)+1
                                    nWSin = self.pyxldata[nWBin]['Worksheets'].index(WS)+1
                                    if nWBin == nWB and nWSin == nWS:
                                        R = self.pyxlnodes[innerlevel][innernode]['row']
                                        C = self.pyxlnodes[innerlevel][innernode]['column']
                                        if (sum([min(R)<=min(item[0])<=max(R),min(R)<=max(item[0])<=max(R)])>0 and\
                                        sum([min(C)<=min(item[1])<=max(C),min(C)<=max(item[1])<=max(C)])>0) or\
                                        (sum([min(item[0])<=min(R)<=max(item[0]),min(item[0])<=max(R)<=max(item[0])])>0 and\
                                        sum([min(item[1])<=min(C)<=max(item[1]),min(item[1])<=max(C)<=max(item[1])])>0):
                                            vec = [i[0] == [level,node] for i in self.intranode]
                                            if not any(vec):
                                                self.intranode.append([[level,node],[[innerlevel,innernode]]])
                                            elif [level,node] not in self.intranode[vec.index(True)][1] and [level, node] != [innerlevel, innernode]:
                                                self.intranode[vec.index(True)][1].append([innerlevel,innernode])
                                            else:
                                                pass
                                        else:
                                            pass
                                    else:
                                        pass

    def hascircularref(self):
        """ inner method hascircularref
            Base method for node/intranode dependency generator
            creates intranode (createintranodes)
            checks for circular references (circularrefwalker)
        """
        print('Starting PyXL circular reference verification...')
        self.circularrefs = []
        t0 = time.time()
        self.createintranodes()
        for index in range(0,len(self.intranode)):
            self.circularrefwalker(index,index,[index])
        if len(self.circularrefs)>0:
            print('{} circular references have been found (elapsed time: {}s)'.format(len(self.circularrefs),time.time()-t0))
            return True
        else:
            print('No circular references have been found (elapsed time: {}s)'.format(time.time()-t0))
            pass
        return False

    def nodeactivator(self,item):
        """ inner method/function nodeactivator
            for node activation
            - activates node
            - checks whether any other node depends on the activated one
            - activates dependent nodes (recursively)
            params (1) : item as pair of integer in list [level,node]
        """
        if item not in self.calcstruct:
            self.calcstruct.append(item)
            vec = [True if item in depedence[1] else False for depedence in self.intranode]
            while any(vec):
                index = vec.index(True)
                self.nodeactivator(dc(self.intranode[index][0]))
                vec[index] = False
        else:
            pass

    def createcalcstruct(self,inputsref,ref=True):
        """ inner method createcalcstruct

        """
        if ref:
            self.calcstruct = []
            self.intranode =[]
            self.circularrefs = []
            self.validatenodes()
            self.hascircularreferences = self.hascircularref()
            print('Beggining of PyXL calculation structure creation...')
            t0 = time.time()
        else:
            pass
        for varyrange in inputsref:
            WB = varyrange[0]
            WS = varyrange[1]
            R = varyrange[2][0]
            C = varyrange[2][1]
            for level in self.pyxlnodes:
               for node in range(0,len(self.pyxlnodes[level])):
                    affected_node = []
                    flag = False
                    nodeobj = self.pyxlnodes[level][node]
                    if nodeobj['dependence'].has_key(WB):
                        if nodeobj['dependence'][WB].has_key(WS):
                            for item in nodeobj['dependence'][WB][WS]:
                                if (sum([min(R)<=min(item[0])<=max(R),min(R)<=max(item[0])<=max(R)])>0 and\
                                sum([min(C)<=min(item[1])<=max(C),min(C)<=max(item[1])<=max(C)])>0) or\
                                (sum([min(item[0])<=min(R)<=max(item[0]),min(item[0])<=max(R)<=max(item[0])])>0 and\
                                sum([min(item[1])<=min(C)<=max(item[1]),min(item[1])<=max(C)<=max(item[1])])>0):
                                    self.nodeactivator([level,node])
                                    nWB = self.pyxldata['Workbooks'].index(nodeobj['filename'])+1
                                    nWS = self.pyxldata[nWB]['Worksheets'].index(nodeobj['sheet'])+1
                                    affected_node.append([nWB,nWS,[nodeobj['row'],nodeobj['column']]])
                                    flag = True
                                    break
            self.createcalcstruct(dc(affected_node),False)
        if ref:
            calcstruct = dc(self.calcstruct)
            intranode = dc(self.intranode)
            dependence = []
            vec = [j[0] for j in intranode]
            for i in calcstruct:
                if i in vec:
                    dependence.append(intranode[vec.index(i)][1])
                else:
                    dependence.append([])
            self.calcstruct = []
            i = 0
            while len(calcstruct)>0:
                flag = False
                flag_circ = False
                for j in range(0,len(calcstruct)):
                    if calcstruct[j] in dependence[i]:
                        if any([calcstruct[i] in [k[0] for k in self.circularrefs]]):
                            flag_circ = True
                            pass
                        else:
                            flag = True
                            break
                    else:
                        pass
                if flag:
                    i += 1
                elif not flag and flag_circ:
                    for k in self.circularrefs:
                        if calcstruct[i] == k[0]:
                            self.calcstruct.append(k[0])
                            self.calcstruct.append(k[1])
                            calcstruct.pop(i)
                            dependence.pop(i)
                            index = calcstruct.index(k[1])
                            calcstruct.pop(index)
                            dependence.pop(index)
                            break
                    i = 0
                else:
                    self.calcstruct.append(calcstruct[i])
                    calcstruct.pop(i)
                    dependence.pop(i)
                    i = 0
            print('Calculation structure created (elapsed time: {}s)'.format(time.time()-t0))
        else:
            pass

    def listconnect(self,itemlist,nWB,nWS):
        """ internal function listconnect
        params (3):
            itemlist as tuple or tuples of tuples
            nWB -> Workbook number as int
            nWS -> Worksheet number as int
        returns a modified version of itemlist with references converted from the
                original XL format to pointing to the converted structure
        """
        if type(itemlist) is tuple or type(itemlist[0]) is tuple:
            if type(itemlist[0]) is tuple:
                itemlist =  [[j for j in i] for i in itemlist]
            else:
                itemlist =  [[i for i in itemlist]]
        else:
            pass
        for i in range(0,len(itemlist)):
            itemlist[i][0] = [self.pyxldata['Workbooks'].index(itemlist[i][0])+1 if itemlist[i][0] != ([] or '') else nWB][0]
            itemlist[i][1] = [[self.pyxldata[itemlist[i][0]]['Worksheets'].index(self.__COM.Workbook.Sheets(itemlist[i][1]).Name)+1 if itemlist[i][1] is not int else itemlist[i][1]][0] if itemlist[i][1] != ([] or '') else nWS][0]
            if not re.compile('R\d+C\d+').search(str(itemlist[i][2])):
                itemlist[i][2] = self.__COM.convert_r1c1A1(itemlist[i][2])[0]
            itemlist[i][2] = [[int(r) for r in re.compile(r'(?<=R)\d+').findall(itemlist[i][2])],[int(c) for c in re.compile(r'(?<=C)\d+').findall(itemlist[i][2])]]
        return itemlist

    def evalstructure(self):
        """ evalstructure
            Evaluates the pyxldata structure based on the calcstruct defined by createcalcstruct.
            It also takes into consideration the existance of circular references in circularrefs.
                - nodes in circular loops are reevaluated until the absolute difference between calculated cells are lesser than 1e-3
        """
        for node in self.calcstruct:
            self.evalpyxlnodes(node[0],node[1])
        if self.hascircularreferences:
            circularrefs = dc(self.circularrefs)
            base = []
            for i in range(0,len(circularrefs)):
                if circularrefs[i][0] not in base:
                    base.append(circularrefs[i][0])
                else:
                    pass
                if circularrefs[i][1] not in base:
                    base.append(circularrefs[i][1])
                else:
                    pass
            circdata = []; dataref = []; delta = []
            for i in base:
                nodeobj = self.pyxlnodes[i[0]][i[1]]
                nWB = self.pyxldata['Workbooks'].index(nodeobj['filename'])+1
                nWS = self.pyxldata[nWB]['Worksheets'].index(nodeobj['sheet'])+1
                for R in range(min(nodeobj['row']),max(nodeobj['row'])+1):
                    for C in range(min(nodeobj['column']),max(nodeobj['column'])+1):
                        circdata.append(self.pyxldata[nWB][nWS][R][C])
                        dataref.append([nWB, nWS, R, C])
            for i in base:
                self.evalpyxlnodes(i[0],i[1])
            for i in range(0,len(dataref)):
                nxtval = self.pyxldata[dataref[i][0]][dataref[i][1]][dataref[i][2]][dataref[i][3]]
                delta.append(np.divide(2*abs(circdata[i]-nxtval),(circdata[i]+nxtval)).tolist())
                circdata[i] = nxtval
            while max(delta)>0.001:
                print(max(delta))
                for i in base:
                    self.evalpyxlnodes(i[0],i[1])
                for i in range(0,len(dataref)):
                    nxtval = self.pyxldata[dataref[i][0]][dataref[i][1]][dataref[i][2]][dataref[i][3]]
                    delta[i] = np.divide(2*abs(circdata[i]-nxtval),(circdata[i]+nxtval)).tolist()
                    circdata[i] = nxtval
        else:
            pass

    def set_io(self,inputsref,ofcell):
        """ set_io
        PyXL solver handler:

        So far only single cell optimization has been included.
        Algorithm parameter allocation is still under development.

        Version 1.0 alpha
            - Single cell O.F.
        """
        if not self.__status__:
            self.createpyxlnodes(ofcell) # create pyxl structure
        else:
            pass
        # convert/link inputsref and ofcell xl references to pyxl structure
        WB = self.__COM.Workbook.Name
        WS = self.__COM.Worksheet.Name
        nWB = self.pyxldata['Workbooks'].index(WB)+1
        nWS = self.pyxldata[nWB]['Worksheets'].index(WS)+1
        # link references to mapped xl cells in pyxldata
        self.iolib['ofcell'] = self.listconnect(ofcell,nWB,nWS)
        self.iolib['inputsref'] = self.listconnect(inputsref,nWB,nWS)
        # create calculation structure/sequence
        self.createcalcstruct(self.iolib['inputsref'])

    def Solver(self,solverparams):
        """ Solver
        This is a anectodal example on how to grab the Objective Function cell ('ofcell') value, modify variables in 'inputsref', recalculate the pyxldata structure and reevaluate 'ofcell'
        """
        # Algorithm Start
        # Flags are True when any addition to the pyxldata structure was mapped, when references have not been included during the object initialozation.
        ofvalue, flag_ofvalue = self.get_pyxlranges(self.iolib['ofcell'])
        seed, flag_seed = self.get_pyxlranges(self.iolib['inputs0ref'])
        stddev, flag_stddev = self.get_pyxlranges(self.iolib['boundsref'])
        # Checks wheter variables- and constraints-references are of the same length
        if inputsref_len.tolist() == inputs0ref_len.tolist() == boundsref_len.tolist():
            # if any flag is True, the following reevaluates the calculation structure
            if any([flag_seed, flag_ofvalue, flag_stddev]):
                self.createcalcstruct(self.iolib['inputsref'])
            else:
                pass
            ofvalue0 = self.get_pyxlranges(self.iolib['ofcell'])[0] # Gets the objective function value from 'ofcell'
            newval = 0 # newval for variables should be parsed from minimization algorithms constrained by 'boundsref'
            self.set_pyxlranges(self.iolib['inputsref'],newval)  # Varuables are update with the newval array
            self.evalstructure() # Structure is recalculated
            ofvalue = self.get_pyxlranges(self.iolib['ofcell'])[0] # new objective function values is assessed
            # Here a loop should proceed to minimize the 'ofcell' by varying 'inputsref' bounded within the 'boundsref' boundaries
        return