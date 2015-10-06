from biokit import GOId, GOTerm, GODB, num2goid



def test_goid():
    goid = GOId(5)
    assert goid.identifier == 'GO:0000005'
    print(goid)
    goid

    assert num2goid(5) == 'GO:0000005'

def test_goterm():
    # Input may be a GO id
    g = GOTerm("GO:0000001")
    assert 'id' in g.to_dict().keys()

    # or OBO
    from bioservices import QuickGO
    q = QuickGO()
    data = q.Term("GO:0000001", frmt='obo')
    g = GOTerm(data)
    g.to_dict()['id']

    # but not yet OBO XML
    data = q.Term("GO:0000001")
    try:
        g = GOTerm(data)
        assert False
    except NotImplementedError:
        assert True

def test_godb():
    g = GODB()
    g.search('insulin')
    g.search('insulin', method='is')
    g.search('insulin', method='startswith')
    g.get_children()
    g.get_children('BP')
    g.get_children('MF')
    g.get_annotations() 
