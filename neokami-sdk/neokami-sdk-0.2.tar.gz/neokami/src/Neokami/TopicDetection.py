''' Copyright 2015 Neokami GmbH. '''

from .NeokamiRequest import NeokamiRequest
from .Exceptions.NeokamiParametersException import NeokamiParametersException
from .HttpClients.NeokamiCurl import NeokamiHttpClient
import six

NeokamiHttpClient = NeokamiHttpClient()

class TopicDetection(NeokamiRequest):

    def upload(self, job_id=None):
        '''
        Upload the text or text array to be analysed
        :param string job_id:
        :return object NeokamiResponse:
        '''
        if (self.checkHasAllParameters(['text'])):
            return self.uploader('/analyse/text/topic/upload', 'text[]', self.text, job_id)


    def analyse(self, job_id):
        '''
        Analyse the text or text array that was uploaded
        :param string job_id:
        :return object NeokamiResponse:
        '''

        return self.analyseFromUpload('/analyse/text/topic', job_id)


    def setText(self, text):
        '''
        Set text to be analyzed
        :param string or list text:
        :return self:
        '''

        if isinstance(text, six.string_types):
            self.text = [text]
        elif isinstance(text, list) and len(text) > 0:
            self.text = text
        else:
            raise NeokamiParametersException('The parameter set is not valid.')

        return self

    def getText(self):
        '''
        Get the text
        :return string text:
        '''
        if hasattr(self, 'text'):
            return self.text
        else:
            raise NeokamiParametersException('Parameter not set.')