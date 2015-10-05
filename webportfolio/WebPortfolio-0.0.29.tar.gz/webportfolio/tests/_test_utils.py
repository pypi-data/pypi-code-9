
import webportfolio.utils as utils


def test_encrypted_string():
    pw = "hello world"
    e = utils.encrypt_string(pw)
    v = utils.verify_encrypted_string(pw, e)
    assert v is True

def test_is_valid_email():
    assert utils.is_valid_email("youder.com") is False
    assert utils.is_valid_email("yo@uder.com") is True
    assert utils.is_valid_email("yo-uder@pp.com") is True
    assert utils.is_valid_email("yo.uder@pp.com") is True
    assert utils.is_valid_email("yo-uder@pp.co.com") is True

def test_to_struct():
    s = utils.to_struct(n="Hello", b="Bye")
    assert s.n == "Hello"