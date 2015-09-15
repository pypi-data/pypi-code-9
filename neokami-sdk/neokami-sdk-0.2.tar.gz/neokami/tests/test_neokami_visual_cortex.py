''' Copyright 2015 Neokami GmbH. '''

import os

from ..src.Neokami.VisualCortex import VisualCortex
from .NeokamiTestCredentials import NeokamiTestCredentials
from .NeokamiTestModel import NeokamiTestModel
from ..src.Neokami.Exceptions.NeokamiParametersException import NeokamiParametersException

import xml.etree.ElementTree as ET
import pytest

class TestNeokamiVisualCortexAnalyserRequest:

    def test_image_from_disk(self):
        req = VisualCortex()
        directory = os.path.dirname(os.path.abspath(__file__))

        req.setFile(directory + '/data/cat1.jpg')
        req.setApiKey(NeokamiTestCredentials.api_key)
        req.setSleep(1)
        req.setModel(NeokamiTestModel.model)
        analysis = req.analyse()
        assert analysis.status() in [200, 408]
        assert 'retries' in analysis.warnings()
        assert analysis.retries() > 0

    def test_image_from_disk_no_wait(self):
        req = VisualCortex()
        directory = os.path.dirname(os.path.abspath(__file__))

        req.setFile(directory + '/data/cat1.jpg')
        req.setWait(0)
        req.setModel(NeokamiTestModel.model)

        req.setApiKey(NeokamiTestCredentials.api_key)
        analysis = req.analyse()
        assert 202 == analysis.status()
        assert 0 == analysis.retries()
        assert 'job_id' in analysis.result()
        assert 'message' in analysis.result()
        assert None == analysis.errors()

        # if a job has been postponed or whatever we get a job id back
        jobId = analysis.result()['job_id']
        reply = req.getResult(jobId)
        # job is either done or not
        assert reply.status() in [200,202]
        assert 0 == len(reply.warnings())
        assert None == reply.errors()

    def test_bytestream_data(self):
        req = VisualCortex()
        req.setApiKey(NeokamiTestCredentials.api_key)

        file = os.path.dirname(os.path.abspath(__file__)) + '/data/cat1.jpg'
        req.setModel(NeokamiTestModel.model)

        f = open(file, 'rb')
        bytestream = f.read()
        req.setStream(bytestream)
        analysis = req.analyseFromStream()
        f.close()

        assert analysis.status() in [200,408]

    def test_bytestream_not_valid(self):
        req =	VisualCortex()

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.setStream([])

        assert 'The stream set is not valid' in str(excinfo.value)


    def test_cascading(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        analysis = VisualCortex().setApiKey(NeokamiTestCredentials.api_key).setFile(directory +'/data/cat1.jpg').setModel(NeokamiTestModel.model).analyse()
        assert analysis.status() in [200, 408]


    def test_data_file_invalid(self):
        req =	VisualCortex()
        req.setFile([])

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.analyse()

        assert 'Invalid file format, file can not be read' in str(excinfo.value)


    def test_no_data(self):
        req = VisualCortex()
        req.setApiKey(NeokamiTestCredentials.api_key)
        reply = req.getResult(1)
        assert reply.hasError()
        assert isinstance(reply.errors(),list)
        assert 0 == len(reply.warnings())


    def test_no_params_disk(self):
        req = VisualCortex()

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.analyseFromDisk()

        assert 'File not set' in str(excinfo.value)


    def test_no_params_stream(self):
        req = VisualCortex()

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.analyseFromStream()

        assert 'Stream not set' in str(excinfo.value)


    def test_data_not_set(self):
        req = VisualCortex()

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.analyse()

        assert 'Missing parameter' in str(excinfo.value)

    def test_feedback_url(self):
        req = VisualCortex()
        url = 'http://cdn01.am.infobae.com/adjuntos/163/imagenes/011/073/0011073719.jpg'
        req.setFile(url)
        req.setLabel('ET')
        req.setApiKey(NeokamiTestCredentials.api_key)
        feedback = req.sendFeedBack()
        assert feedback.status() in [202, 408]

    def test_feedback_base64(self):
        req = VisualCortex()
        directory = os.path.dirname(os.path.abspath(__file__))
        req.setFile(directory + '/data/cat1.jpg')

        req.setFeedbackType('base64')
        req.setLabel('cat')
        req.setApiKey(NeokamiTestCredentials.api_key)
        feedback = req.sendFeedBack()
        assert feedback.status() in [202, 408]

    def test_feedback_no_data(self):
        req = VisualCortex()

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.sendFeedBack()

        assert 'Missing parameter' in str(excinfo.value)
