"""
Test functions for rn.py

Copyright (C) 2015 Jose M. Casarejos

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

You may contact the author of the program at: <rn-program@mundo-r.com>
"""
import sys
import os
import glob
from rn import *


#
# testdir
#   |
#   |-- members: Graham Chapman, John Cleese, Terry Gilliam, Eric Idle,
#   |            Terry Jones, Michael Palin
#   |
#   |-- movies
#   |      |
#   |      |-- Flying Circus
#   |      |-- Life of Brian
#   |      |-- The Holy Grail
#   |                |- Arthur, Lancelot, Patsy, Robin, Galahad
#   |-- special: *asterisk, ?question, [brackets]


def test_delete_first():
    """
    Don't test wrong values.
    The function doesn't check for wrong values so they should not
    be passed to it.
    """
    text = 'Flying Circus'
    # good values
    assert delete_first(1, text) == 'lying Circus'
    assert delete_first(3, text) == 'ing Circus'
    assert delete_first(7, text) == 'Circus'
    assert delete_first(10, text) == 'cus'
    # boundary conditions
    assert delete_first(9999, text) == ''
    assert delete_first(99999999, text) == ''


def test_delete_last():
    """
    Don't test wrong values.
    The function doesn't check for wrong values so they should not
    be passed to it.
    """
    text = 'Flying Circus'
    # good values
    assert delete_last(1, text) == 'Flying Circu'
    assert delete_last(3, text) == 'Flying Cir'
    assert delete_last(7, text) == 'Flying'
    assert delete_last(10, text) == 'Fly'
    # boundary conditions
    assert delete_last(9999, text) == ''
    assert delete_last(99999999, text) == ''


def test_delete_middle():
    """
    Don't test wrong values.
    The function doesn't check for wrong values so they should not
    be passed to it.
    """
    text = 'Flying Circus'
    # good values
    assert delete_middle(1, 3, text) == 'ing Circus'
    assert delete_middle(3, 4, text) == 'Flng Circus'
    assert delete_middle(7, 15, text) == 'Flying'
    assert delete_middle(10, 10, text) == 'Flying Cicus'
    # boundary conditions
    assert delete_middle(10, 99, text) == 'Flying Ci'
    assert delete_middle(1, 9999, text) == ''
    assert delete_middle(99, 9999, text) == text


def test_delete_from():
    """
    Don't test wrong values.
    The function doesn't check for wrong values so they should not
    be passed to it.
    """
    text = 'Flying Circus'
    # good values
    assert delete_from(1, text) == ''
    assert delete_from(3, text) == 'Fl'
    assert delete_from(7, text) == 'Flying'
    assert delete_from(10, text) == 'Flying Ci'
    # boundary conditions
    assert delete_from(99, text) == text
    assert delete_from(9999, text) == text


def test_delete():
    list = ['Circus', 'Grail', 'Brian', 'Life', 'SpamAlot']
    empty_list = ['' for i in range(5)]

    # val = n / :n
    # good values
    assert delete('1', list) == ['ircus', 'rail', 'rian', 'ife', 'pamAlot']
    assert delete('3', list) == ['cus', 'il', 'an', 'e', 'mAlot']
    assert delete('7', list) == ['', '', '', '', 't']
    assert delete(':1', list) == ['ircus', 'rail', 'rian', 'ife', 'pamAlot']
    assert delete(':3', list) == ['cus', 'il', 'an', 'e', 'mAlot']
    assert delete(':7', list) == ['', '', '', '', 't']
    # boundary conditions
    assert delete('10', list) == empty_list
    assert delete(':10', list) == empty_list
    assert delete('99', list) == empty_list
    assert delete(':99', list) == empty_list
    assert delete('9999', list) == empty_list
    assert delete(':9999', list) == empty_list
    # wrong values
    wrong_list = ['0', ':0', 'a', ':a', 'text', ':text']
    for arg in wrong_list:
        try:
            delete(arg, list)
        except ValueError:
            assert True
        else:
            assert False

    # val = -n
    # good values
    assert delete('-1', list) == ['Circu', 'Grai', 'Bria', 'Lif', 'SpamAlo']
    assert delete('-3', list) == ['Cir', 'Gr', 'Br', 'L', 'SpamA']
    assert delete('-7', list) == ['', '', '', '', 'S']
    # bounday conditions
    assert delete('-10', list) == empty_list
    assert delete('-99', list) == empty_list
    assert delete('-9999', list) == empty_list
    # wrong values
    wrong_list = ['-0', '-a', '-text']
    for arg in wrong_list:
        try:
            delete(arg, list)
        except ValueError:
            assert True
        else:
            assert False

    # val = n:
    # good values
    assert delete('3:', list) == ['Ci', 'Gr', 'Br', 'Li', 'Sp']
    assert delete('7:', list) == ['Circus', 'Grail', 'Brian', 'Life', 'SpamAl']
    # bounday conditions
    assert delete('1:', list) == empty_list
    assert delete('10:', list) == list
    assert delete('99:', list) == list
    assert delete('9999:', list) == list
    # wrong values
    wrong_list = ['0:', 'a:', 'text:']
    for arg in wrong_list:
        try:
            delete(arg, list)
        except ValueError:
            assert True
        else:
            assert False

    # val = n:m
    # good values
    assert delete('1:3', list) == ['cus', 'il', 'an', 'e', 'mAlot']
    assert delete('3:4', list) == ['Cius', 'Grl', 'Brn', 'Li', 'SpAlot']
    assert delete('3:3', list) == ['Cicus', 'Gril', 'Bran', 'Lie',
                                   'SpmAlot']
    assert delete('7:15', list) == ['Circus', 'Grail', 'Brian', 'Life',
                                    'SpamAl']
    # boundary conditions
    assert delete('10:10', list) == list
    assert delete('10:99', list) == list
    assert delete('1:99', list) == empty_list
    assert delete('99:9999', list) == list
    # wrong values
    wrong_list = ['0:0', '0:3', '3:0', '7:5', '-1:-2', '-2:-4', 'a:e', '-a:e']
    for arg in wrong_list:
        try:
            delete(arg, list)
        except ValueError:
            assert True
        else:
            assert False


def test_crop_text():
    """
    Don't test wrong values.
    The function doesn't check for wrong values so they should not
    be passed to it.
    """
    text = 'Flying Circus'
    # good values
    assert crop_text('Fly', text) == 'ing Circus'
    assert crop_text('Flying', text) == ' Circus'
    assert crop_text('Cir', text) == 'Flying cus'
    assert crop_text('Circus', text) == 'Flying '
    assert crop_text('c', text) == 'Flying Cirus'
    assert crop_text('i', text) == 'Flyng Crcus'
    # bounday values
    assert crop_text(text, text) == ''
    assert crop_text('', text) == text
    assert crop_text('Brian', text) == text
    # mixed case - function is case sensitive
    assert crop_text('f', text) == text
    assert crop_text('Y', text) == text
    assert crop_text('F', text) == 'lying Circus'
    # input with white space or other delimiter
    text = "Monty-Python's : Flying_Circus"
    assert crop_text(':', text) == "Monty-Python's  Flying_Circus"
    assert crop_text('-', text) == "MontyPython's : Flying_Circus"
    assert crop_text(' ', text) == "Monty-Python's:Flying_Circus"
    assert crop_text('_', text) == "Monty-Python's : FlyingCircus"


def test_crop_to():
    """
    Don't test wrong values.
    The function doesn't check for wrong values so they should not
    be passed to it.
    """
    text = 'Flying Circus'
    # good values
    assert crop_to('Fly', text) == 'ing Circus'
    assert crop_to('Flying', text) == ' Circus'
    assert crop_to('Cir', text) == 'cus'
    assert crop_to('Circus', text) == ''
    assert crop_to('c', text) == 'us'
    assert crop_to('i', text) == 'ng Circus'
    # boundary values
    assert crop_to(text, text) == ''
    assert crop_to('', text) == text
    assert crop_to('Brian', text) == text
    # mixed case - function is case sensitive (this version?)
    assert crop_to('y', text) == 'ing Circus'
    assert crop_to('Y', text) == text
    # input with white space or other delimiter
    text = "Monty-Python's : Flying_Circus"
    assert crop_to(':', text) == " Flying_Circus"
    assert crop_to('-', text) == "Python's : Flying_Circus"
    assert crop_to(' ', text) == ": Flying_Circus"
    assert crop_to('_', text) == "Circus"


def test_crop_from():
    """
    Don't test wrong values.
    The function doesn't check for wrong values so they should not
    be passed to it.
    """
    text = 'Flying Circus'
    # good values
    assert crop_from('Fly', text) == ''
    assert crop_from('Flying', text) == ''
    assert crop_from('Cir', text) == 'Flying '
    assert crop_from('Circus', text) == 'Flying '
    assert crop_from('c', text) == 'Flying Cir'
    assert crop_from('i', text) == 'Fly'
    # boundary values
    assert crop_from(text, text) == ''
    assert crop_from('Brian', text) == text
    # mixed case - function is case sensitive (this version?)
    assert crop_from('y', text) == 'Fl'
    assert crop_from('Y', text) == text
    # input with white space or other delimiter
    text = "Monty-Python's : Flying_Circus"
    assert crop_from(':', text) == "Monty-Python's "
    assert crop_from('-', text) == "Monty"
    assert crop_from(' ', text) == "Monty-Python's"
    assert crop_from('_', text) == "Monty-Python's : Flying"


def test_crop_middle():
    """
    Don't test wrong values.
    The function doesn't check for wrong values so they should not
    be passed to it.
    """
    text = 'Flying Circus'
    # good values
    assert crop_middle('Fly', 'Cir', text) == 'cus'
    assert crop_middle('Flying', 'Circus', text) == ''
    assert crop_middle('Cir', 'u', text) == 'Flying s'
    assert crop_middle('c', 'u', text) == 'Flying Cirs'
    assert crop_middle('i', 'C', text) == 'Flyircus'
    # boundary values
    assert crop_middle(text, text, text) == text
    assert crop_middle('', '', text) == text
    assert crop_middle('Circus', '', text) == 'Flying '  # like -x Circus:
    assert crop_middle('', 'Circus', text) == ''  # like -x :Circus
    assert crop_middle('Bri', 'an', text) == text
    # mixed case - function is case sensitive (this version?)
    assert crop_middle('y', 'C', text) == 'Flircus'
    assert crop_middle('y', 'c', text) == 'Flus'
    # input with white space or other delimiter
    text = "Monty-Python's : Flying_Circus"
    assert crop_middle(':', '_', text) == "Monty-Python's Circus"
    assert crop_middle('-', '_', text) == "MontyCircus"
    assert crop_middle(' ', ' ', text) == "Monty-Python'sFlying_Circus"
    assert crop_middle('_', 's', text) == "Monty-Python's : Flying"
    assert crop_middle('-', ':', text) == "Monty Flying_Circus"


def test_crop():
    list = ['Circus', 'Grail', 'Brian', 'Life', 'SpamAlot']
    # text
    assert crop('i', list) == ['Crcus', 'Gral', 'Bran', 'Lfe', 'SpamAlot']
    # text:
    assert crop('i:', list) == ['C', 'Gra', 'Br', 'L', 'SpamAlot']
    # :text
    assert crop(':i', list) == ['rcus', 'l', 'an', 'fe', 'SpamAlot']
    # text1:text2
    assert crop('r:i', list) == ['Circus', 'Gl', 'Ban', 'Life', 'SpamAlot']
    assert crop('i:r', list) == ['Ccus', 'Grail', 'Brian', 'Life', 'SpamAlot']
    # text doesn't exist
    assert crop('z', list) == list
    assert crop(':z', list) == list
    assert crop('z:', list) == list
    # empty space
    assert crop('', list) == list
    assert crop('"":""', list) == list
    assert crop(':""', list) == list
    assert crop('"":', list) == list
    list = ["Monty-Python's : Flying_Circus"]
    # interpreted as crop_from('-:',list)
    assert crop('-::', list) == ["Monty-Python's : Flying_Circus"]
    # interpreted as crop_from ' :'
    assert crop(' ::', list) == ["Monty-Python's"]


def test_replace():
    list = ['Circus', 'Grail', 'Brian', 'Life', 'SpamAlot']
    assert replace('i', '1', list) == ['C1rcus', 'Gra1l', 'Br1an', 'L1fe',
                                       'SpamAlot']
    # text doesn't exist
    assert replace('z', '0', list) == list
    # empty options
    wrong_list = [['', 'e'], ['e', ''], ['', '']]
    for arg in wrong_list:
        try:
            assert replace(arg[0], arg[1], list) == list
        except ValueError:
            assert True
    assert replace('e', '3', list) == ['Circus', 'Grail', 'Brian', 'Lif3',
                                       'SpamAlot']
    assert replace('E', '3', list) == list
    # symbols
    list = ["Monty-Python's : Flying_Circus"]
    assert replace('-', ' ', list) == ["Monty Python's : Flying_Circus"]


def test_upper():
    list = ['Circus', 'Grail', 'Brian', 'Life', 'SpamAlot']
    assert upper(list) == ['CIRCUS', 'GRAIL', 'BRIAN', 'LIFE', 'SPAMALOT']


def test_lower():
    list = ['Circus', 'Grail', 'Brian', 'Life', 'SpamAlot']
    assert lower(list) == ['circus', 'grail', 'brian', 'life', 'spamalot']


def test_title():
    list = ['circus', 'grail', 'brian', 'life', 'spamalot']
    assert title(list) == ['Circus', 'Grail', 'Brian', 'Life', 'Spamalot']


def test_add_prefix():
    list = ['Circus', 'Grail', 'Brian', 'Life', 'SpamAlot']
    assert add_prefix('MP-', list) == ['MP-Circus', 'MP-Grail', 'MP-Brian',
                                       'MP-Life', 'MP-SpamAlot']


def test_add_suffix():
    list = ['Circus', 'Grail', 'Brian', 'Life', 'SpamAlot']
    assert add_suffix('-MP', list) == ['Circus-MP', 'Grail-MP', 'Brian-MP',
                                       'Life-MP', 'SpamAlot-MP']


def test_split_file():
    list = [os.sep + os.path.join('monty-python', 'movies', 'old',
                                  'Flying.Circus')]
    assert split_file(list) == ([os. sep + os.path.join('monty-python',
                                                        'movies', 'old')],
                                ['Flying'],
                                ['Circus'])
    list = [os.sep + os.path.join('monty-python', 'movies', 'old')]
    assert split_file(list) == ([os.sep + os.path.join('monty-python',
                                                       'movies')],
                                ['old'], [''])
    list = [os.sep + os.path.join('monty-python', 'movies', 'old') + os.sep]
    assert split_file(list) == ([os.sep + os.path.join('monty-python',
                                                       'movies', 'old')],
                                [''], [''])
    list = ['']
    assert split_file(list) == ([''], [''], [''])
    list = [os.sep]
    assert split_file(list) == ([os.sep], [''], [''])
    list = ['Flying.Circus']
    assert split_file(list) == ([''], ['Flying'], ['Circus'])


def test_split_dir():
    list = [os.sep + os.path.join('monty-python', 'movies', 'old')]
    assert split_dir(list) == ([os.sep + os.path.join('monty-python',
                               'movies')], ['old'])
    list = [os.sep + os.path.join('monty-python', 'movies')]
    assert split_dir(list) == ([os.sep + os.path.join('monty-python')],
                               ['movies'])
    list = [os.sep + os.path.join('monty-python', 'movies', 'old') + os.sep]
    assert split_dir(list) == ([os.sep + os.path.join('monty-python',
                                                      'movies', 'old')],
                               [''])
    list = ['']
    assert split_dir(list) == ([''], [''])
    list = [os.sep]
    assert split_dir(list) == ([os.sep], [''])
    list = ['Flying.Circus']
    assert split_dir(list) == ([''], ['Flying.Circus'])


# test directory created by test program
#
# testdir
#   |
#   |-- members: Graham Chapman, John Cleese, Terry Gilliam, Eric Idle,
#   |            Terry Jones, Michael Palin
#   |
#   |-- movies
#          |
#          |-- Flying Circus
#          |-- Life of Brian
#          |-- The Holy Grail
#                    |- Arthur, Lancelot, Patsy, Robin, Galahad
#


def test_select_directories():
    os.chdir('testdir')
    # existing directories
    list = ['members', 'movies']
    assert select_directories(list) == list
    list = ['members', 'movies', os.path.join('movies', 'The Holy Grail')]
    assert select_directories(list) == list
    list = ['members', 'movies', os.path.join('movies', 'The Holy Grail')]
    assert select_directories(list) == list
    list = glob.glob('*' + os.sep + '*')
    assert select_directories(list) == [os.path.join('movies',
                                                     'Flying Circus'),
                                        os.path.join('movies',
                                                     'Life of Brian'),
                                        os.path.join('movies',
                                                     'The Holy Grail')]
    # directory doesn't exist
    list = ['producers', 'actors']
    assert select_directories(list) == []
    list = ['producers', 'movies']
    assert select_directories(list) == ['movies']
    os.chdir(os.pardir)


def test_select_files():
    os.chdir('testdir')
    # existing files
    list = glob.glob('*' + os.sep + '*' + os.sep + '*')
    assert select_files(list) == [os.path.join('movies', 'The Holy Grail',
                                               'Arthur'),
                                  os.path.join('movies', 'The Holy Grail',
                                               'Galahad'),
                                  os.path.join('movies', 'The Holy Grail',
                                               'Lancelot'),
                                  os.path.join('movies', 'The Holy Grail',
                                               'Patsy'),
                                  os.path.join('movies', 'The Holy Grail',
                                               'Robin')]
    list = ['members', 'movies']
    assert select_files(list) == []
    list = ['members', 'movies', os.path.join('movies', 'The Holy Grail',
                                              'Arthur')]
    assert select_files(list) == [os.path.join('movies', 'The Holy Grail',
                                               'Arthur')]
    # file doesn't exist
    list = [os.path.join('movies', 'The Meaning of Life')]
    assert select_files(list) == []
    os.chdir(os.pardir)


def test_select_extensions():
    os.chdir('testdir')
    # five files, five extensions (blank extensions)
    list = glob.glob('*' + os.sep + '*' + os.sep + '*')
    assert select_extensions(list) == ['', '', '', '', '']
    # no files, no extensions
    list = glob.glob('*')
    assert select_extensions(list) == []
    # one file, one extension
    os.rename(os.path.join('movies', 'The Holy Grail', 'Arthur'),
              os.path.join('movies', 'The Holy Grail', 'Arthur.King'))
    list = ['movies', 'members', os.path.join('movies', 'The Holy Grail',
                                              'Arthur.King')]
    assert select_extensions(list) == ['King']
    # restore file names
    os.rename(os.path.join('movies', 'The Holy Grail', 'Arthur.King'),
              os.path.join('movies', 'The Holy Grail', 'Arthur'))
    os.chdir(os.pardir)


def test_check_unique():
    # not repeated elements
    list = [os.path.join('movies', 'Flying Circus'),
            os.path.join('movies', 'Life of Brian'),
            os.path.join('movies', 'The Holy Grail')]
    assert check_unique(list) is True
    # repeated elements
    list = [os.path.join('movies', 'Flying Circus'),
            os.path.join('movies', 'Life of Brian'),
            os.path.join('movies', 'The Holy Grail'),
            os.path.join('movies', 'Flying Circus')]
    assert check_unique(list) is False


def test_rename():
    os.chdir('testdir')
    # files
    # new names, not existing files
    old = [os.path.join('movies', 'The Holy Grail', 'Arthur'),
           os.path.join('movies', 'The Holy Grail', 'Lancelot'),
           os.path.join('movies', 'The Holy Grail', 'Patsy'),
           os.path.join('movies', 'The Holy Grail', 'Robin'),
           os.path.join('movies', 'The Holy Grail', 'Galahad')]
    new = [os.path.join('movies', 'The Holy Grail', 'Arthuro'),
           os.path.join('movies', 'The Holy Grail', 'Lancelote'),
           os.path.join('movies', 'The Holy Grail', 'Patsya'),
           os.path.join('movies', 'The Holy Grail', 'Robina'),
           os.path.join('movies', 'The Holy Grail', 'Galahada')]
    try:
        rename(old, new)
    except OSError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthuro'))
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Robina'))
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Galahad')) is False
    # revert
    old = [os.path.join('movies', 'The Holy Grail', 'Arthuro'),
           os.path.join('movies', 'The Holy Grail', 'Lancelote'),
           os.path.join('movies', 'The Holy Grail', 'Patsya'),
           os.path.join('movies', 'The Holy Grail', 'Robina'),
           os.path.join('movies', 'The Holy Grail', 'Galahada')]
    new = [os.path.join('movies', 'The Holy Grail', 'Arthur'),
           os.path.join('movies', 'The Holy Grail', 'Lancelot'),
           os.path.join('movies', 'The Holy Grail', 'Patsy'),
           os.path.join('movies', 'The Holy Grail', 'Robin'),
           os.path.join('movies', 'The Holy Grail', 'Galahad')]
    rename(old, new)
    # new name, existing file
    old = [os.path.join('movies', 'The Holy Grail', 'Arthur')]
    new = [os.path.join('movies', 'The Holy Grail', 'Galahad')]
    try:
        rename(old, new)
    except FileExistsError:
        assert True
    else:
        assert False
    # repeated name, not existing file
    old = [os.path.join('movies', 'The Holy Grail', 'Arthur'),
           os.path.join('movies', 'The Holy Grail', 'Galahad')]
    new = [os.path.join('movies', 'The Holy Grail', 'Galahad'),
           os.path.join('movies', 'The Holy Grail', 'Galahad')]
    try:
        rename(old, new)
    except FileExistsError:
        assert True
    else:
        assert False
    # new file name, existing dir
    old = [os.path.join('movies', 'movies.txt')]
    new = [os.path.join('movies', 'Life of Brian')]
    try:
        rename(old, new)
    except FileExistsError:
        assert True
    else:
        assert False
    # extensions
    # new extensions, not existing files
    old = [os.path.join('movies', 'The Holy Grail', 'Arthur'),
           os.path.join('movies', 'The Holy Grail', 'Lancelot'),
           os.path.join('movies', 'The Holy Grail', 'Patsy'),
           os.path.join('movies', 'The Holy Grail', 'Robin'),
           os.path.join('movies', 'The Holy Grail', 'Galahad')]
    new = [os.path.join('movies', 'The Holy Grail', 'Arthur.o'),
           os.path.join('movies', 'The Holy Grail', 'Lancelot.e'),
           os.path.join('movies', 'The Holy Grail', 'Patsy.a'),
           os.path.join('movies', 'The Holy Grail', 'Robin.a'),
           os.path.join('movies', 'The Holy Grail', 'Galahad.a')]
    try:
        rename(old, new)
    except OSError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Lancelot.e'))
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Galahad.a'))
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthur')) is False
    # revert
    old = [os.path.join('movies', 'The Holy Grail', 'Arthur.o'),
           os.path.join('movies', 'The Holy Grail', 'Lancelot.e'),
           os.path.join('movies', 'The Holy Grail', 'Patsy.a'),
           os.path.join('movies', 'The Holy Grail', 'Robin.a'),
           os.path.join('movies', 'The Holy Grail', 'Galahad.a')]
    new = [os.path.join('movies', 'The Holy Grail', 'Arthur'),
           os.path.join('movies', 'The Holy Grail', 'Lancelot'),
           os.path.join('movies', 'The Holy Grail', 'Patsy'),
           os.path.join('movies', 'The Holy Grail', 'Robin'),
           os.path.join('movies', 'The Holy Grail', 'Galahad')]
    rename(old, new)
    os.chdir(os.pardir)
    # directories
    # new names, not existing dirs
    old = [os.path.join('movies', 'Flying Circus'),
           os.path.join('movies', 'Life of Brian'),
           os.path.join('movies', 'The Holy Grail')]
    new = [os.path.join('movies', 'Circus'),
           os.path.join('movies', 'Brian'),
           os.path.join('movies', 'Grail')]
    os.chdir('testdir')
    try:
        rename(old, new)
    except OSError:
        assert False
    else:
        assert True
    assert os.path.isdir(os.path.join('movies', 'Circus'))
    assert os.path.isdir(os.path.join('movies', 'Brian'))
    assert os.path.isdir(os.path.join('movies', 'Life of Brian')) is False
    # revert
    old = [os.path.join('movies', 'Circus'),
           os.path.join('movies', 'Brian'),
           os.path.join('movies', 'Grail')]
    new = [os.path.join('movies', 'Flying Circus'),
           os.path.join('movies', 'Life of Brian'),
           os.path.join('movies', 'The Holy Grail')]
    rename(old, new)
    # new name, existing dir
    old = [os.path.join('movies', 'Flying Circus')]
    new = [os.path.join('movies', 'Life of Brian')]
    try:
        rename(old, new)
    except FileExistsError:
        assert True
    else:
        assert False
    # repeated name, not existing dir
    old = [os.path.join('movies', 'The Holy Grail'),
           os.path.join('movies', 'Life of Brian')]
    new = [os.path.join('movies', 'Life of Brian'),
           os.path.join('movies', 'The Holy Grail')]
    try:
        rename(old, new)
    except FileExistsError:
        assert True
    else:
        assert False
    # new dir, existing file
    old = [os.path.join('movies', 'Flying Circus')]
    new = [os.path.join('movies', 'movies.txt')]
    try:
        rename(old, new)
    except FileExistsError:
        assert True
    else:
        assert False
    os.chdir(os.pardir)


def test_parse():
    os.chdir('testdir')
    # good values
    files = glob.glob('*')
    arg = '-d 1 '.split() + files
    assert parse(arg) == {
        'help': False,
        'delete': '1', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': False, 'ext': False, 'quiet': False,
        'files': ['members', 'movies', 'special']
        }
    os.chdir(os.path.join('movies', 'The Holy Grail'))
    arg = '-d 1 Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '1', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': False, 'ext': False, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-x word Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '', 'crop': 'word', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': False, 'ext': False, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-r word1 word2 Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '', 'crop': '', 'replace': ['word1', 'word2'],
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': False, 'ext': False, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-u Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '', 'crop': '', 'replace': '',
        'upper': True, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': False, 'ext': False, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-l Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '', 'crop': '', 'replace': '',
        'upper': False, 'lower': True, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': False, 'ext': False, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-t Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': True,
        'prefix': False, 'suffix': False,
        'dir': False, 'ext': False, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-p prefix Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': 'prefix', 'suffix': False,
        'dir': False, 'ext': False, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-s suffix Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': 'suffix',
        'dir': False, 'ext': False, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-d 1 --dir Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '1', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': True, 'ext': False, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-d 1 --ext Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '1', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': False, 'ext': True, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-d 1 -q Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '1', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': False, 'ext': False, 'quiet': True,
        'files': ['Arthur']
        }
    arg = '-d 1 --dir -q Arthur'.split()
    assert parse(arg) == {
        'help': False,
        'delete': '1', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': True, 'ext': False, 'quiet': True,
        'files': ['Arthur']
        }
    arg = '-d 1 -q --dir Arthur'.split()     # different order
    assert parse(arg) == {
        'help': False,
        'delete': '1', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': True, 'ext': False, 'quiet': True,
        'files': ['Arthur']
        }
    # wrong values
    # missing mandatory argument
    files = glob.glob('*')
    wrong_list = ['--dir ' + ' '.join(files), '-q *' ' '.join(files),
                  '-q --ext']
    for arg in wrong_list:
        try:
            parse(arg.split())
        except ValueError:
            assert True
        else:
            assert False
    # missing values
    wrong_list = ['-d Arthur', '-r word1 Arthur', '-x Arthur']
    for arg in wrong_list:
        try:
            parse(arg.split())
        except ValueError:
            assert True
        else:
            assert False
    # extra arguments
    # in windows takes extra args as files but glob won't catch
    # them as files unless there are really files/dirs with that names
    arg = '-d 3 -x word Arthur'.split()
    if sys.platform.startswith('win'):
        assert parse(arg) == {
            'help': False,
            'delete': '3', 'crop': '', 'replace': '',
            'upper': False, 'lower': False, 'title': False,
            'prefix': False, 'suffix': False,
            'dir': False, 'ext': False, 'quiet': False,
            'files': ['Arthur']
            }
    else:
        assert parse(arg) == {
            'help': False,
            'delete': '3', 'crop': '', 'replace': '',
            'upper': False, 'lower': False, 'title': False,
            'prefix': False, 'suffix': False,
            'dir': False, 'ext': False, 'quiet': False,
            'files': ['-x', 'Arthur', 'word']
            }
    arg = '--dir -d 1 Arthur'.split()    # order not correct
    try:
        parse(arg)
    except ValueError:
        assert True
    else:
        assert False
    # contradictory orders
    arg = '-d 1 --dir --ext Arthur'.split()      # last target prevails
    assert parse(arg) == {
        'help': False,
        'delete': '1', 'crop': '', 'replace': '',
        'upper': False, 'lower': False, 'title': False,
        'prefix': False, 'suffix': False,
        'dir': False, 'ext': True, 'quiet': False,
        'files': ['Arthur']
        }
    arg = '-u -l -t Arthur'.split()      # upper > lower > title
    if sys.platform.startswith('win'):
        assert parse(arg) == {
            'help': False,
            'delete': '', 'crop': '', 'replace': '',
            'upper': True, 'lower': False, 'title': False,
            'prefix': False, 'suffix': False,
            'dir': False, 'ext': False, 'quiet': False,
            'files': ['Arthur']
            }
    else:
        assert parse(arg) == {
            'help': False,
            'delete': '', 'crop': '', 'replace': '',
            'upper': True, 'lower': False, 'title': False,
            'prefix': False, 'suffix': False,
            'dir': False, 'ext': False, 'quiet': False,
            'files': ['-l', '-t', 'Arthur']
            }
    os.chdir(os.pardir)
    os.chdir(os.pardir)
    # test the brackets problem
    os.chdir('special')
    if sys.platform.startswith('win'):
        arg = '-l *'.split()
        assert parse(arg) == {
            'help': False,
            'delete': '', 'crop': '', 'replace': '',
            'upper': False, 'lower': True, 'title': False,
            'prefix': False, 'suffix': False,
            'dir': False, 'ext': False, 'quiet': False,
            'files': ['[brackets]', 'asterisk', 'question']
            }
        # no file like to [*] with [ as a wildcard for glob.glob
        arg = '-l [*]'.split()
        assert parse(arg) == {
            'help': False,
            'delete': '', 'crop': '', 'replace': '',
            'upper': False, 'lower': True, 'title': False,
            'prefix': False, 'suffix': False,
            'dir': False, 'ext': False, 'quiet': False,
            'files': []
            }
        arg = '-l [*'.split()
        assert parse(arg) == {
            'help': False,
            'delete': '', 'crop': '', 'replace': '',
            'upper': False, 'lower': True, 'title': False,
            'prefix': False, 'suffix': False,
            'dir': False, 'ext': False, 'quiet': False,
            'files': ['[brackets]']
            }
    else:
        files = glob.glob('*')    # simulate O.S. wildcard expansion
        arg = ['-l'] + files
        assert parse(arg) == {
            'help': False,
            'delete': '', 'crop': '', 'replace': '',
            'upper': False, 'lower': True, 'title': False,
            'prefix': False, 'suffix': False,
            'dir': False, 'ext': False, 'quiet': False,
            'files': ['*asterisk', '?question', '[brackets]']
            }
        files = glob.glob('[*]')
        arg = ['-l'] + files
        try:
            assert parse(arg) == {
                'help': False,
                'delete': '', 'crop': '', 'replace': '',
                'upper': False, 'lower': True, 'title': False,
                'prefix': False, 'suffix': False,
                'dir': False, 'ext': False, 'quiet': False,
                'files': ['[brackets]']
                }
        except ValueError:
            assert True
        else:
            assert False
        files = glob.glob('[*')
        arg = ['-l'] + files
        assert parse(arg) == {
            'help': False,
            'delete': '', 'crop': '', 'replace': '',
            'upper': False, 'lower': True, 'title': False,
            'prefix': False, 'suffix': False,
            'dir': False, 'ext': False, 'quiet': False,
            'files': ['[brackets]']
            }
    os.chdir(os.pardir)
    os.chdir(os.pardir)


def test_main():
    os.chdir('testdir')
    # good values
    # target file
    try:
        main(['-d', '1', '-q', os.path.join('movies', 'The Holy Grail',
                                            'Arthur')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'rthur'))
    try:
        main(['-x', 'r', '-q', os.path.join('movies', 'The Holy Grail',
                                            'rthur')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail', 'thu'))
    try:
        main(['-r', 'thu', 'Arthur', '-q',
              os.path.join('movies', 'The Holy Grail', 'thu')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthur'))
    try:
        main(['-u', '-q', os.path.join('movies', 'The Holy Grail',
                                       'Arthur')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'ARTHUR'))
    try:
        main(['-l', '-q', os.path.join('movies', 'The Holy Grail',
                                       'ARTHUR')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'arthur'))
    try:
        main(['-t', '-q', os.path.join('movies', 'The Holy Grail',
                                       'arthur')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthur'))
    try:
        main(['-p', 'prefix', '-q', os.path.join('movies', 'The Holy Grail',
                                                 'Arthur')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'prefixArthur'))
    try:
        main(['-s', 'suffix', '-q',
              os.path.join('movies', 'The Holy Grail', 'prefixArthur')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'prefixArthursuffix'))
    # revert
    os.rename(os.path.join('movies', 'The Holy Grail',
                           'prefixArthursuffix'),
              os.path.join('movies', 'The Holy Grail', 'Arthur'))
    # target directory
    try:
        main('-d 1 -q --dir movies'.split())
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isdir('ovies')
    try:
        main('-x i -q --dir ovies'.split())
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isdir('oves')
    try:
        main('-r oves movies -q --dir oves'.split())
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isdir('oves') is False
    assert os.path.isdir('movies')
    try:
        main('-u -q --dir members'.split())
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isdir('MEMBERS')
    try:
        main('-l -q --dir MEMBERS'.split())
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isdir('members')
    try:
        main('-t -q --dir members'.split())
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isdir('Members')
    try:
        main('-p prefix -q --dir Members'.split())
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isdir('prefixMembers')
    try:
        main('-s suffix -q --dir prefixMembers'.split())
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isdir('prefixMemberssuffix')
    # target extension
    os.rename(os.path.join('movies', 'The Holy Grail', 'Arthur'),
              os.path.join('movies', 'The Holy Grail', 'Arthur.King'))
    try:
        main(['-d', '2', '-q', '--ext', os.path.join('movies',
              'The Holy Grail', 'Arthur.King')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthur.ng'))
    try:
        main(['-r', 'ng', 'King', '-q', '--ext',
              os.path.join('movies', 'The Holy Grail', 'Arthur.ng')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthur.King'))
    try:
        main(['-u', '-q', '--ext',
              os.path.join('movies', 'The Holy Grail', 'Arthur.King')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthur.KING'))
    try:
        main(['-l', '-q', '--ext',
              os.path.join('movies', 'The Holy Grail', 'Arthur.KING')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthur.king'))
    try:
        main(['-t', '-q', '--ext',
             os.path.join('movies', 'The Holy Grail', 'Arthur.king')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthur.King'))
    try:
        main(['-p', 'prefix', '-q', '--ext',
              os.path.join('movies', 'The Holy Grail', 'Arthur.King')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthur.prefixKing'))
    try:
        main(['-s', 'suffix', '-q', '--ext',
              os.path.join('movies', 'The Holy Grail',
                           'Arthur.prefixKing')])
    except ValueError:
        assert False
    else:
        assert True
    assert os.path.isfile(os.path.join('movies', 'The Holy Grail',
                                       'Arthur.prefixKingsuffix'))
    # wrong arguments
    files = glob.glob('*')
    wrong_list = ['', '-argument', '-d', '-d 1', '-d a ' + ' '.join(files),
                  '-r word1']
    for arg in wrong_list:
        try:
            main(arg.split())
        except ValueError:
            assert True
        else:
            assert False
    # revert
    os.rename(os.path.join('movies', 'The Holy Grail',
                           'Arthur.prefixKingsuffix'),
              os.path.join('movies', 'The Holy Grail',
                           'Arthur'))
