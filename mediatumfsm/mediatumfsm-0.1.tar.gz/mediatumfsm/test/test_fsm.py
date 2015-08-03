# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from pytest import fixture, raises
from mediatumfsm.fsm import MessageNotAccepted, State
from mediatumfsm.test import accumulatorfsm
from mediatumfsm.test.accumulatorfsm import Accumulator, AcceptInt, AcceptStr, Nothing, Int, Str
from mediatumfsm.test.regexfsm import RegexFSM

### fixtures

@fixture
def fsm():
    return Accumulator()

@fixture
def fsm_with_name():
    return Accumulator(name="test")

@fixture
def fsm_int():
    return Accumulator("Int", (23, None))

@fixture
def fsm_str():
    return Accumulator("Str", "spam")

@fixture
def fsm_regex():
    return RegexFSM()

### tests

def test_init(fsm):
    assert fsm.initial_data == False
    assert fsm.initial_state == Nothing


def test_can_access_states_in_module(fsm):
    assert issubclass(accumulatorfsm.Nothing, State)  # @UndefinedVariable
    assert issubclass(accumulatorfsm.Int, State)  # @UndefinedVariable
    assert issubclass(accumulatorfsm.Str, State)  # @UndefinedVariable

def test_init_with_values(fsm_int):
    assert fsm_int.data == (23, None)
    assert fsm_int.state == Int


def test_switch_to_str(fsm):
    state = fsm.send(AcceptStr())
    assert state == fsm.state == Str


def test_accept_str_value(fsm_str):
    fsm_str.send("|eggs")
    assert fsm_str.data == "spam|eggs"
    assert fsm_str.state == Str


def test_switch_to_int_from_str(fsm_str):
    fsm_str.send(AcceptInt())
    assert fsm_str.state == Int
    assert fsm_str.data == (0, None)


def test_handler_with_condition_int(fsm_int):
    fsm_int.send(23)
    assert fsm_int.data == (46, "odd")
    fsm_int.send(358)
    assert fsm_int.data == (404, "even")


def test_on_transition(fsm):
    accumulatorfsm.switched_to_int_times = 0
    fsm.send(AcceptInt())
    assert accumulatorfsm.switched_to_int_times == 1
    fsm.send(AcceptInt())
    assert accumulatorfsm.switched_to_int_times == 1


def test_regexfsm(fsm_regex):
    inputstr = "aaaaRSGTEgtfvok*fswgBBBGEGHTEG#"
    fsm_regex.parse(inputstr)
    assert fsm_regex.stopped

### failure tests

def test_wrong_message_type(fsm_int):
    with raises(MessageNotAccepted):
        fsm_int.send(dict())


def test_unhandled_case_wrong_value(fsm_int):
    with raises(ValueError):
        fsm_int.send("wrong string is wrong type")


def test_regexfsm_malformed_input(fsm_regex):
    malformed_inputs = [
         "aaRSGTEgtfvok*fswgBBBGEGHTEG#",
         "bla",
         "#",
         ]
    for inp in malformed_inputs:
        with raises(MessageNotAccepted):
            print("testing malformed string " + inp)
            fsm_regex.parse(inp)


def test_regexfsm_incomplete_input(fsm_regex):
    incomplete_inputs = [
         "",
         "a",
         "aaa",
         "aaaarghkrogkG",
         ]
    for inp in incomplete_inputs:
        print("testing malformed string " + inp)
        fsm_regex.parse(inp)
        assert not fsm_regex.stopped

### pydot

def test_pydot(fsm):
    fsm.create_graph(add_unhandled_case_handlers=True)
    result = fsm.dot()
    print(result)
    assert "digraph" in result
    assert "AcceptInt" in result
    assert "Accumulator" in result
    assert "m % 2 == 1" in result
    assert "even" in result
    assert "color=black" in result
    assert "color=green" in result
    assert "style=dashed" in result
