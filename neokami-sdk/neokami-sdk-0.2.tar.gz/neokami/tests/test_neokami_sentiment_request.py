''' Copyright 2015 Neokami GmbH. '''

from ..src.Neokami.SentimentAnalyser import SentimentAnalyser
from .NeokamiTestCredentials import NeokamiTestCredentials
from ..src.Neokami.Exceptions.NeokamiParametersException import NeokamiParametersException

import pytest


class TestNeokamiSentimentAnalyserRequest:
	def test_text(self):
		req = SentimentAnalyser()

		req.setText("I am not what you think I am. I am not what I think I am. I am what I think you think I am.")
		req.setApiKey(NeokamiTestCredentials.api_key)
		req.setSleep(1)
		analysis = req.analyse()
		assert analysis.status() in [200, 408]
		assert 'retries' in analysis.warnings()
		assert analysis.retries() > 0


	def test_split_text(self):
		req = SentimentAnalyser()

		req.setText("I am not what you think I am. I am not what I think I am. I am what I think you think I am.")
		req.setApiKey(NeokamiTestCredentials.api_key)
		req.setSplitText()
		req.setSleep(1)
		analysis = req.analyse()
		assert analysis.status() in [200, 408]
		assert 'retries' in analysis.warnings()
		assert analysis.retries() > 0

	def test_text_no_wait(self):
		req = SentimentAnalyser()

		req.setText("I am not what you think I am. I am not what I think I am. I am what I think you think I am.")
		req.setApiKey(NeokamiTestCredentials.api_key)
		req.setSleep(1)
		req.setWait(0)
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



	def test_cascading(self):
		analysis = SentimentAnalyser().setApiKey(NeokamiTestCredentials.api_key).setText("I am not what you think I am. I am not what I think I am. I am what I think you think I am.").analyse()
		assert analysis.status() in [200, 408]


	def test_data_text_invalid(self):
		req =	SentimentAnalyser()

		with pytest.raises(NeokamiParametersException) as excinfo:
			req.setText([])

		assert 'The text set is not valid' in str(excinfo.value)

	def test_no_data(self):
		req = SentimentAnalyser()
		req.setApiKey(NeokamiTestCredentials.api_key)

		reply = req.getResult(1)
		assert reply.hasError()
		assert isinstance(reply.errors(),list)
		assert 0 == len(reply.warnings())

	def test_no_params(self):
		req = SentimentAnalyser()

		with pytest.raises(NeokamiParametersException) as excinfo:
			req.analyse()

		assert 'Missing parameter: text' in str(excinfo.value)
