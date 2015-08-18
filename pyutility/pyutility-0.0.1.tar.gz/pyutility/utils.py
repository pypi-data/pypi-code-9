import itertools

def showList(li,  restrict=10):
    nPrint = restrict if restrict <= len(li) else len(li)
    #pdb.set_trace()
    li = list(li)
    strPrint = ', '.join(li[:(restrict-1)])
    if nPrint>0:
        if nPrint < len(li):
            print "***Top %d elements: ***\n%s" % (nPrint,  strPrint)
        else:
            print "***Identified %d elements: ***\n%s" % (nPrint,  strPrint)
    else:
        pass

def compareNames(list1,  list2,  restrict=50,  name1='list 1',  name2='list 2'):
    """
    compare two list of strings
    
    """
    just1 = set(list1) - set(list2)
    just2 = set(list2) - set(list1)
    shared = set(list1) & set(list2)
    #pdb.set_trace()
    print "%d total elements in %s; %d total elements in %s" % (len(list1),  name1,  len(list2),  name2)
    print "\n%d elements only in %s" %(len(just1),  name1)
    showList(just1,  restrict=restrict)
    print "\n%d elements shared in %s and %s" %(len(shared),  name1,  name2)
    showList(shared,  restrict=restrict)
    print "\n%d elements only in %s" %(len(just2),  name2)
    showList(just2,  restrict=restrict)


#compareNames(df_countryByRegion['name_chinese'].tolist(),  df_countryByRegion1['name_chinese'].tolist(), name1='Old version', name2='Current version')

def showDuplicatedElements0(c):
    '''sort/tee/izip'''
    a, b = itertools.tee(sorted(c))
    next(b, None)
    r = None
    for k, g in itertools.izip(a, b):
        if k == g:
            if k != r:
                yield k
                r = k


def showDuplicatedElements(c,  restrict=10):
    dup = list(showDuplicatedElements0(c))
    print "%d duplicated elements" % (len(dup))
    showList(dup,  restrict=restrict)
