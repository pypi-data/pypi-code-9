''' Copyright 2015 Neokami GmbH. '''

from ..src.Neokami.TopicDetection import TopicDetection
from .NeokamiTestCredentials import NeokamiTestCredentials
from ..src.Neokami.Exceptions.NeokamiParametersException import NeokamiParametersException

import pytest


class TestNeokamiTopicDetectionRequest:

	def test_text(self):

		req = TopicDetection()

		req.setText("I am not what you think I am. I am not what I think I am. I am what I think you think I am.")
		req.setApiKey(NeokamiTestCredentials.api_key)
		req.setSleep(1)
		upload = req.upload()
		assert upload.status() is 202

		job_id = upload.result()['job_id']
		upload2 = req.upload(job_id)
		assert upload2.status() is 202

		analysis = req.analyse(job_id)

		assert analysis.status() in [200, 408]
		assert 'retries' in analysis.warnings()
		assert analysis.retries() > 0


	def test_array_text(self):
		req = TopicDetection()
		texts_array = ["I am not what you think I am. I am not what I think I am. I am what I think you think I am.",
					   "I am lazy I do not want to write more",
					   "Damn! I need another element"]
		req.setText(texts_array)
		req.setApiKey(NeokamiTestCredentials.api_key)
		req.setSleep(1)
		upload = req.upload()
		assert upload.status() is 202

		job_id = upload.result()['job_id']
		req.setText("I am not what you think I am. I am not what I think I am. I am what I think you think I am.")
		upload2 = req.upload(job_id)
		assert upload2.status() is 202

		analysis = req.analyse(job_id)

		assert analysis.status() in [200, 408]
		assert 'retries' in analysis.warnings()
		assert analysis.retries() > 0

	def test_cascading(self):
		upload = TopicDetection().setApiKey(NeokamiTestCredentials.api_key).\
			setText("I am not what you think I am. I am not what I think I am. I am what I think you think I am.").\
			upload()

		assert upload.status() is 202


	def test_data_text_invalid(self):
		req =	TopicDetection()

		with pytest.raises(NeokamiParametersException) as excinfo:
			req.setText([])

		assert 'The parameter set is not valid' in str(excinfo.value)

	def test_no_data(self):
		req = TopicDetection()
		req.setApiKey(NeokamiTestCredentials.api_key)

		reply = req.getResult(1)
		assert reply.hasError()
		assert isinstance(reply.errors(),list)
		assert 0 == len(reply.warnings())

	def test_no_params(self):
		req = TopicDetection()

		with pytest.raises(NeokamiParametersException) as excinfo:
			req.upload()

		assert 'Missing parameter: text' in str(excinfo.value)

