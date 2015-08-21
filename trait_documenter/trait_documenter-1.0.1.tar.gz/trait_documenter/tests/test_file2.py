from traits.api import Event, Float, Int, List

from . import test_file

test_file.Event = Event

constant = 1

trait_1 = Event

if False:

    trait_2 = List(Float)

if True:

    #: inside definition
    trait_2 = List(Int)

    #: another definition
    trait_3 = List(Float)
