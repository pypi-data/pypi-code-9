''' Copyright 2015 Neokami GmbH. '''

import os

from ..src.Neokami.ImageAnalyser import ImageAnalyser
from .NeokamiTestCredentials import NeokamiTestCredentials
from ..src.Neokami.Exceptions.NeokamiParametersException import NeokamiParametersException

import xml.etree.ElementTree as ET
import pytest


class TestNeokamiImageAnalyserRequest:
    def test_image_from_disk(self):
        req = ImageAnalyser()
        directory = os.path.dirname(os.path.abspath(__file__))

        req.setFile(directory + '/data/team1.jpg')
        req.setApiKey(NeokamiTestCredentials.api_key)
        req.setSleep(1)
        req.setType('gender')
        analysis = req.analyseFromDisk()
        assert analysis.status() in [200, 408]
        assert 'retries' in analysis.warnings()
        assert analysis.retries() > 0

    def test_image_from_disk_no_wait(self):
        req = ImageAnalyser()
        directory = os.path.dirname(os.path.abspath(__file__))

        req.setFile(directory + '/data/team1.jpg')
        req.setWait(0)
        req.setType('gender')
        req.setApiKey(NeokamiTestCredentials.api_key)
        analysis = req.analyseFromDisk()
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
        req = ImageAnalyser()
        req.setApiKey(NeokamiTestCredentials.api_key)

        file = os.path.dirname(os.path.abspath(__file__)) + '/data/team1.jpg'
        req.setType('gender')
        f = open(file, 'rb')
        bytestream = f.read()
        req.setStream(bytestream)
        analysis = req.analyseFromStream()
        f.close()

        assert analysis.status() in [200,408]

    def test_bytestream_not_valid(self):
        req =	ImageAnalyser()

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.setStream([])

        assert 'The stream set is not valid' in str(excinfo.value)


    def test_cascading(self):
        directory = os.path.dirname(os.path.abspath(__file__))
        analysis = ImageAnalyser().setApiKey(NeokamiTestCredentials.api_key).setFile(directory +'/data/team1.jpg').setType('gender').analyse()
        assert analysis.status() in [200, 408]


    def test_data_file_invalid(self):
        req =	ImageAnalyser()
        req.setFile([])

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.analyse()

        assert 'Invalid file format, file can not be read' in str(excinfo.value)


    def test_no_data(self):
        req = ImageAnalyser()
        req.setApiKey(NeokamiTestCredentials.api_key)
        reply = req.getResult(1)
        assert reply.hasError()
        assert isinstance(reply.errors(),list)
        assert 0 == len(reply.warnings())


    def test_output_types(self):
        req = ImageAnalyser()
        req.setApiKey(NeokamiTestCredentials.api_key)
        directory = os.path.dirname(os.path.abspath(__file__))

        req.setFile(directory + '/data/team1.jpg')
        req.setWait(0)
        req.setOutputType('memory')
        analysis = req.analyseFromDisk()
        assert 202 == analysis.status()


    def test_output_types_falsy(self):
        req = ImageAnalyser()
        req.setApiKey(NeokamiTestCredentials.api_key)
        directory = os.path.dirname(os.path.abspath(__file__))
        req.setFile(directory + '/data/team1.jpg')

        req.setWait(0)
        with pytest.raises(NeokamiParametersException) as excinfo:
            req.setOutputType('invalid')

        assert 'Specified output is not valid.' in str(excinfo.value)


    def test_output_format_xml(self):
        req = ImageAnalyser()
        req.setApiKey(NeokamiTestCredentials.api_key)
        directory = os.path.dirname(os.path.abspath(__file__))
        req.setFile(directory + '/data/team1.jpg')
        req.setWait(0)
        req.setOutputFormat('xml')
        analysis = req.analyseFromDisk()
        data = analysis.result()
        ET.fromstring(data) #no exception raise --> xml well formed

        assert data != None


    def test_output_format_json(self):
        req = ImageAnalyser()
        req.setApiKey(NeokamiTestCredentials.api_key)
        directory = os.path.dirname(os.path.abspath(__file__))
        req.setFile(directory + '/data/team1.jpg')
        req.setWait(1)
        req.setOutputFormat('json')
        analysis = req.analyseFromDisk()
        data = analysis.result()
        assert data != None


    def test_no_params_disk(self):
        req = ImageAnalyser()

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.analyseFromDisk()

        assert 'File not set' in str(excinfo.value)


    def test_no_params_stream(self):
        req = ImageAnalyser()

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.analyseFromStream()

        assert 'Stream not set' in str(excinfo.value)


    def test_data_not_set(self):
        req = ImageAnalyser()

        with pytest.raises(NeokamiParametersException) as excinfo:
            req.analyse()

        assert 'Missing parameter' in str(excinfo.value)
