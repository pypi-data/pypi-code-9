import pytest
from ttr.rdsutils.rds_sort import get_rdstime

lines = """2406046AE0CD4749;33;40;92.6 MHz;2015-08-12T10:36:31Z
24062469692E2043;33;40;92.6 MHz;2015-08-12T10:36:31Z
2406046FE0CD4E41;31;40;92.6 MHz;2015-08-12T10:36:32Z
""".strip().splitlines()


@pytest.fixture(params=lines)
def rdsline_correct(request):
    return request.param


def create_tmp_rds_file(tmpdir, rds_line, mode="oneline"):
    """In tmpdir create sample rds file with given line

    mode controls, what other lines are present:
        ok_modes = ["oneline", "oneline_nonl", "garbagefirst", "garbagelast"]
        null_modes = ["empty", "garbageonly"]
    """

    fname = tmpdir / mode + ".rds"
    with fname.open("w") as f:
        if mode == "oneline":
            f.write(rds_line + "\n")
        elif mode == "oneline_nonl":
            f.write(rds_line)
        elif mode == "garbagefirst":
            garbage = "GarbageDataHere\n"
            for i in range(3):
                f.write(garbage)
            f.write(rds_line)
        elif mode == "garbagelast":
            f.write(rds_line + "\n")
            garbage = "GarbageDataHere\n"
            for i in range(3):
                f.write(garbage)
        elif mode == "empty":
            pass
        elif mode == "garbageonly":
            garbage = "GarbageDataHere\n"
            for i in range(3):
                f.write(garbage)
    return fname


def test_get_rdstime(rdsline_correct, tmpdir):
    exp_time = rdsline_correct.strip().split(";")[4]
    msg = "expected timestamp string shall be 20 chars long"
    assert len(exp_time) == 20, msg

    ok_modes = ["oneline", "oneline_nonl", "garbagefirst", "garbagelast"]
    null_modes = ["empty", "garbageonly"]
    for mode in ok_modes:
        tmp_rds_file = create_tmp_rds_file(tmpdir, rdsline_correct, mode)
        ts = get_rdstime(tmp_rds_file)
        assert ts == exp_time
    for mode in null_modes:
        tmp_rds_file = create_tmp_rds_file(tmpdir, rdsline_correct, mode)
        ts = get_rdstime(tmp_rds_file)
        assert ts is None
