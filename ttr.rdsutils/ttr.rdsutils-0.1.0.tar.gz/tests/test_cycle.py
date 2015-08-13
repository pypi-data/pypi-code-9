import pytest
from ttr.rdsutils.rds_cycle import formatline

lines = """2406046AE0CD4749;33;40;92.6 MHz;2015-08-12T10:36:31Z
24062469692E2043;33;40;92.6 MHz;2015-08-12T10:36:31Z
2406046FE0CD4E41;31;40;92.6 MHz;2015-08-12T10:36:32Z
""".strip().splitlines()


@pytest.fixture(params=lines)
def rdsline_correct(request):
    return request.param


def test_formatline_correct(rdsline_correct):
    ctime = 0.0
    ctimestr = "1970-01-01T00:00:00"
    org_itms = rdsline_correct.split(";")
    res = formatline(rdsline_correct, ctime)
    itms = res.split(";")
    assert len(itms) == 5
    assert res.startswith(";".join(org_itms[:4]))
    assert itms[4].startswith(ctimestr)
