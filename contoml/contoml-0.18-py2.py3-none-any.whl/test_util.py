from contoml.util import is_sequence_like, is_dict_like

def test_is_sequence_like():
    assert is_sequence_like([1, 3, 4])
    assert not is_sequence_like(42)
    

def test_is_dict_like():
    assert is_dict_like({'name': False})
    assert not is_dict_like(42)
    assert not is_dict_like([4, 8, 15])
