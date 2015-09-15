''' Copyright 2015 Neokami GmbH. '''

from .NeokamiRequest import NeokamiRequest
from .NeokamiResponse import NeokamiResponse
from .Exceptions.NeokamiParametersException import NeokamiParametersException
from .HttpClients.NeokamiCurl import NeokamiHttpClient

NeokamiHttpClient = NeokamiHttpClient()

import six

class SentimentAnalyser(NeokamiRequest):

	split = 0

	def analyse(self):
		'''
		Analyse text
		:return object NeokamiResponse:
		'''

		if (self.checkHasAllParameters(['text'])):
			response = NeokamiHttpClient.post(
				self.getUrl('/analyse/text/sentiment'),
				self.getApiKey(),
				{
					'wait': self.getWait(),
					'max_retries': self.getMaxRetries(),
					'sleep': self.getSleep(),
					'sdk_version': self.SDK_VERSION,
					'sdk_lang': self.SDK_LANG,
					'text': self.text,
					'sentences':self.split
				}
			)

			return NeokamiResponse(response, self.getOutputFormat(), self.getSilentFails())


	def setSplitText(self, isSplit=True):
		'''
		Set value to split or not the result in sentences
		;param bool isSplit:
		:return self:
		'''

		if(isSplit): self.split = 1
		else: self.split = 0

		return self

	def setText(self, text):
		'''
		Set text to be analyzed
		:param string text:
		:return self:
		'''
		if isinstance(text, six.string_types):
			self.text = text
		else:
			raise NeokamiParametersException('The text set is not valid.')

		return self

	def getSplitText(self):
		'''
		Get the split value
		:return bool:
		'''
		if(self.split == 1): return True
		else: return False

	def getText(self):
		'''
		Get the text
		:return string text:
		'''
		if hasattr(self, 'text'):
			return self.text
		else:
			raise NeokamiParametersException('Text not set.')