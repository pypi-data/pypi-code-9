
from pprint import pprint
from . import grouped, pluralized, overlapped, chunked

def assertequal(correct, output):
    try:
        assert correct == output
    except AssertionError:
        pprint(correct)
        print('\n!=\n')
        pprint(output)
        print('\n')

        raise

def test_grouped():
    objects = [{'id': 1, 'foo': 'bar'},
               {'id': 1, 'foo': 'baz'},
               {'id': 2, 'foo': 'qux'}]

    first, second, third = objects

    groupeddict = dict(grouped(((obj['id'], obj['foo'])
                            for obj in objects)))

    groupedlist = list(grouped(((obj['id'], obj)
                                for obj in objects)))

    assertequal({1: ['bar', 'baz'], 2: ['qux']},
                groupeddict)

    assertequal([(1, [first, second]), (2, [third])],
                groupedlist)

def test_pluralized():
    dict_  = {}
    list_  = [{}]
    tuple_ = ({},)

    assertequal([{}], list(pluralized(dict_)))

    assertequal([{}], list(pluralized(list_)))

    assertequal([({},)], list(pluralized(tuple_)))

def test_overlapped():
    assertequal([], list(overlapped([])))
    assertequal([], list(overlapped([1])))
    assertequal([(1, 2)], list(overlapped([1, 2])))
    assertequal([(1, 2), (2, 3)], list(overlapped([1, 2, 3])))
    assertequal([(1, 2), (2, 3), (3, 4)], list(overlapped([1, 2, 3, 4])))

if __name__ == '__main__':
    test_grouped()
    test_pluralized()
    test_overlapped()

    print('ok')
