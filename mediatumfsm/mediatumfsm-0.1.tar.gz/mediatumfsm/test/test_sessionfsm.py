# -*- coding: utf-8 -*-
from __future__ import absolute_import
from pytest import fixture
from mediatumfsm.test.accumulatorfsm import Accumulator, AcceptStr, Str

### fixtures

@fixture
def session():
    s = Accumulator.session
    s.clear()
    return s

@fixture
def fsm():
    return Accumulator()

@fixture
def fsm_with_name():
    return Accumulator(name="test")


### tests

def test_state_saving(fsm, session):
    fsm.send(AcceptStr())
    assert session["state_data"] == ""
    assert session["current_state"] == "Str"
    fsm.send("spam")
    assert session["state_data"] == "spam"
    new_fsm = Accumulator.from_saved_state()
    assert new_fsm.data == "spam"
    assert new_fsm.state == Str


def test_state_saving_named_fsm(fsm_with_name, session):
    fsm_with_name.send(AcceptStr())
    assert session["test"]["state_data"] == ""
    assert session["test"]["current_state"] == "Str"
    fsm_with_name.send("spam")
    assert session["test"]["state_data"] == "spam"
    new_fsm = Accumulator.from_saved_state("test")
    # compares name, state and data equality
    assert new_fsm == fsm_with_name
