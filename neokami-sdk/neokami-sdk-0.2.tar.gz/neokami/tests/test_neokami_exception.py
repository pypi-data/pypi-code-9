''' Copyright 2015 Neokami GmbH. '''

import os

from ..src.Neokami.ImageAnalyser import ImageAnalyser
from ..src.Neokami.Exceptions.NeokamiAuthorizationException import NeokamiAuthorizationException
from six import string_types
import pytest


class TestNeokamiException:
    def test_authorization_exception_silent(self):
        req = ImageAnalyser()
        directory = os.path.dirname(os.path.abspath(__file__))
        req.setFile(directory + '/data/team1.jpg')
        req.setWait(0)
        req.setSilentFails(True)
        analysis = req.analyseFromDisk()

        assert analysis.hasError()
        assert analysis.status() == 401
        assert analysis.result() == None

        req.setApiKey('invalid')
        assert analysis.hasError()
        assert analysis.status() == 401
        assert analysis.result() == None
        assert isinstance(analysis.errors(), list)


    def test_authorization_exception(self):
        req = ImageAnalyser()
        directory = os.path.dirname(os.path.abspath(__file__))
        req.setFile(directory + '/data/team1.jpg')
        req.setWait(0)
        req.setApiKey(None)

        with pytest.raises(NeokamiAuthorizationException) as excinfo:
            req.analyseFromDisk()

        assert 'Api key is not valid!' in str(excinfo.value)

    def test_authorization_exception(self):
        req = ImageAnalyser()
        directory = os.path.dirname(os.path.abspath(__file__))
        req.setFile(directory + '/data/team1.jpg')
        req.setWait(0)
        req.setApiKey('invalid')

        with pytest.raises(NeokamiAuthorizationException) as excinfo:
            req.analyseFromDisk()

        assert 'This API key cannot access this function!' in str(excinfo.value)


    def test_authorization_exception_format(self):
        try:
            req = ImageAnalyser()
            directory = os.path.dirname(os.path.abspath(__file__))
            req.setFile(directory + '/data/team1.jpg')
            req.setWait(0)
            req.setApiKey('invalid')
            req.analyseFromDisk()

        except NeokamiAuthorizationException as e:
            msg, code = e.args

            assert isinstance(msg, string_types)
            assert code == 401
            assert not e.isMalformed()
            assert 0 == len(e.getWarnings())
            assert 1 == len(e.getError())

