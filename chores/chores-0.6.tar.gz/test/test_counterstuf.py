from chores.counterstuf import counterstuf

def test_counterstuf():
    """Test counterstuf class"""
    c = counterstuf()
    c.update("this and this is this but that isn't this".split())
    c.total = sum(c.values())
    assert c.total == 9
    assert c.this == 4
    assert c.but == 1
    assert c.bozo == 0
    c2 = counterstuf().update_self("big big small big medium xlarge".split())
    assert c2.medium == 1
    assert dict(c2.most_common()) == dict([('big', 3), ('small', 1), ('medium', 1), ('xlarge', 1)])