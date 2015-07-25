
from chores import *
import time

def test_tally_simple():
    todos = Chores()
    todos.mark('one', 'good')
    todos.mark('two', 'good')
    todos.mark('three', 'bad')

    tally = todos.tally()
    assert tally.good == 2
    assert tally.good == todos.count('good')
    assert todos.marked('good') == ['one', 'two']

def test_bystatus():
    todos = Chores()
    todos.mark('one', 'good')
    todos.mark('two', 'good')
    todos.mark('three', 'bad')
    todos.mark('four', 'error')
    todos.mark('five', 'good')

    listed = todos.bystatus()
    assert listed.good == ['one', 'two', 'five']
    assert listed.bad == ['three']
    assert listed.error == ['four']

def test_access():

    todos = Chores()
    todos.mark('one', 'good')
    todos.mark('two', 'good')
    todos.mark('three', 'bad')

    assert todos['two'].status == 'good'
    todos['one'].status = 'stuff'
    assert todos['one'].status == 'stuff'
    assert todos.count('good') == 1
    assert todos.count('stuff') == 1

    # print s.report("POSTACCESS", total='TOTAL')

def test_data():
    todos = Chores()
    todos.mark('one', 'good')
    todos.mark('two', 'good')
    todos.mark('three', 'bad')

    for chore_id in todos:
        todos.data(chore_id).upper = chore_id.upper()
        todos.data(chore_id).lower = chore_id.lower()

    for chore_id in todos:
        assert todos.data(chore_id).upper == chore_id.upper()
        assert todos.data(chore_id).lower == chore_id.lower()

def test_direct_data():
    todos = Chores()
    todos.mark('one', 'good')
    todos.mark('two', 'good')
    todos.mark('three', 'bad')

    for t in todos.values():
        t.upcase = t.id.upper()

    for chore_id in todos:
        assert todos[chore_id].upcase == chore_id.upper()

def test_multi_mark():
    s = Chores()
    good = ['a', 'b', 'c']
    bad  = ['d', 'e']
    ugly = ['f', 'g']

    s.mark(good, 'good')
    s.mark(bad, 'bad')
    s.mark(ugly, 'ugly')
    assert s.marked('good') == good
    assert s.marked('bad') == bad
    assert s.marked(('good', 'bad')) == good + bad
    assert s.marked('ugly') == ugly
    assert s.marked(('good', 'ugly')) == good + ugly
    assert s.marked(('bad', 'ugly')) == bad + ugly

    assert s.marked('good', exclude='bad') == good
    assert s.marked(('good', 'bad'), exclude='bad') == good
    assert s.marked('good', exclude='ugly') == good
    assert s.marked(('good', 'bad', 'ugly'), exclude='ugly') == good + bad
    assert s.marked(('good', 'bad', 'ugly'), exclude='bad') == good + ugly


    s.mark('d', 'good')
    assert s['d'].status == 'good'
    s.mark(['a', 'c', 'f'], 'error')
    assert s.count('error') == 3
    assert s.count('good') == 2

def test_string_selection():
    s = Chores()
    good = ['a', 'b', 'c']
    bad  = ['d', 'e']
    ugly = ['f', 'g']
    s.mark(good, 'good')
    s.mark(bad, 'bad')
    s.mark(ugly, 'ugly')


    assert s.marked('good|bad') == good + bad
    assert s.marked('good|ugly') == good + ugly
    assert s.marked('bad|ugly') == bad + ugly

    assert s.marked('^bad') == good + ugly
    assert s.marked('^ugly') == good + bad
    assert s.marked('^ugly|bad') == good
    assert s.marked('^good|bad') == ugly


def test_target_statuses():
    s = Chores()
    s.mark('a', 'good')
    s.mark('b', 'good')
    s.mark('c', 'bad')
    s.mark('d', 'error')

    assert s.statuses() == 'good bad error'.split()
    assert s._target_statuses() == set('good bad error'.split())

    assert s._target_statuses('good') == set(['good'])
    assert s._target_statuses('bad') == set(['bad'])
    assert s._target_statuses('error') == set(['error'])

    assert s._target_statuses('good bad'.split()) == set(['good', 'bad'])
    assert s._target_statuses('bad error'.split()) == set(['bad', 'error'])
    assert s._target_statuses('good error'.split()) == set(['good', 'error'])

    assert s._target_statuses(exclude='good')  == set('bad error'.split())
    assert s._target_statuses(exclude='bad')   == set('good error'.split())
    assert s._target_statuses(exclude='error') == set('good bad'.split())

def test_exclude():

    s = Chores()
    s.mark('a', 'good')
    s.mark('b', 'good')
    s.mark('c', 'bad')
    s.mark('d', 'error')

    assert s.marked('good')  == s.marked(exclude='bad error'.split())
    assert s.marked('bad')   == s.marked(exclude='good error'.split())
    assert s.marked('error') == s.marked(exclude='good bad'.split())
    assert s.marked(['bad', 'error']) == s.marked(exclude='good')

def test_iteration():
    s = Chores('one two three four five'.split())
    indices = []
    names  = []
    for index, item in enumerate(s):
        s.mark(item, 'injested')
        indices.append(index)
        names.append(item)
    assert indices == [0, 1, 2, 3, 4]
    assert names  == 'one two three four five'.split()

def test_doc_example_one():

    from chores import Chores

    chores = Chores('Jones able baker charlie 8348 Smith Brown Davis'.split())

    for c in chores:
        status = 'name' if c.istitle() else 'other'
        chores.mark(c, status)


    assert chores.marked('name') == ['Jones', 'Smith', 'Brown', 'Davis']
    assert chores.count('name') == 4
    assert chores.marked(exclude='name') == [ 'able', 'baker', 'charlie', '8348']
    assert chores.count(exclude='name') == 4

    assert chores.marked('^name') == chores.marked(exclude='name')
    assert chores.count('^name') == chores.count(exclude='name')


def test_name_and_repr():
    s = Chores(name='Julian')
    assert repr(s) == "Chores('Julian')"

    s = Chores()
    r = repr(s)
    assert r.startswith("Chores('0x")
    assert r.endswith("')")

def test_len():

    s = Chores()
    assert len(s) == 0

    s = Chores(range(1))
    assert len(s) == 1

    s = Chores(range(10))
    assert len(s) == 10


def test_add_during_iteration():
    s = Chores('one two three four five'.split())
    for index, item in enumerate(s, start=1):
        if index == 3:
            s.add('error', 'ERROR')
        elif index % 2 == 0 and item != 'error':
            s.mark(item, 'even')

    assert s.statuses() == ['new', 'even', 'ERROR']
    assert s.count('new') == 3
    assert s.count('even') == 2
    assert s.count('ERROR') == 1
