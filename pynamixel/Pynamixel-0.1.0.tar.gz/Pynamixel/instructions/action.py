# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>


class ActionResponse(object):
    """
    @todoc
    """
    def __init__(self, parameters):
        assert len(parameters) == 0


class Action(object):
    """
    @todoc
    """
    code = 0x05
    parameters = []
    response_class = ActionResponse
