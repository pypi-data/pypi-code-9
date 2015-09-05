# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>


class ResetResponse(object):
    """
    @todoc
    """
    def __init__(self, parameters):
        assert len(parameters) == 0


class Reset(object):
    """
    @todoc
    """
    code = 0x06
    parameters = []
    response_class = ResetResponse
