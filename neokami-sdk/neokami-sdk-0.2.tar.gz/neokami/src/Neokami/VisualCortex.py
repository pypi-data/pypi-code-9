''' Copyright 2015 Neokami GmbH. '''

from .NeokamiRequest import NeokamiRequest
from .NeokamiResponse import NeokamiResponse
from .Exceptions.NeokamiParametersException import NeokamiParametersException
from .HttpClients.NeokamiCurl import NeokamiHttpClient

NeokamiHttpClient = NeokamiHttpClient()

import base64

class VisualCortex(NeokamiRequest):
    API_BASE = 'https://api.visualcortex.io'
    max_retries = 100
    model = None
    type = 'custom'
    label = None
    feedbackType = None

    def getUrl(self, path):
        return self.API_BASE + path

    def analyse(self):
        '''
        Analyse an image depending on whether or the image was set using a file path or a bytestream
        :return object NeokamiResponse:
        '''
        if (self.checkHasAllParameters(['file'])):
            return self.analyseFromDisk()

        elif (self.checkHasAllParameters(['stream'])):
            return self.analyseFromStream()
        else:
            raise NeokamiParametersException('Not file nor stream set. Please set one of those two options.')


    def analyseFromDisk(self):
        '''
        Analyse image from file path
        :return object NeokamiResponse:
        '''

        bytestream = self.getByteStreamFromFilePath(self.getFile())

        response = self.postBinary(bytestream)
        return NeokamiResponse(response, self.getOutputFormat(), self.getSilentFails())


    def analyseFromStream(self):
        '''
        Analyse image from bytestream
        :return object NeokamiResponse:
        '''

        bytestream = self.getStream()

        response = self.postBinary(bytestream)
        return NeokamiResponse(response, self.getOutputFormat(), self.getSilentFails())

    def postBinary(self, bytestream):
        '''
        Post bytestream
        :param bytestream:
        :return <Response>:
        '''
        return NeokamiHttpClient.postBinary(
            self.getUrl('/cortex/analyse'),
            bytestream,
            self.getApiKey(),
            {
                'wait': self.getWait(),
                'max_retries': self.getMaxRetries(),
                'sleep': self.getSleep(),
                'type': self.getType(),
                'sdk_version': self.SDK_VERSION,
                'sdk_lang': self.SDK_LANG,
                'model': self.getModel()
            }
        )


    def getByteStreamFromFilePath(self, filePath):
        '''
        Get bytestream from image stored on your system
        :param string filePath:
        :return bytestream data:
        '''
        try:
            with open(filePath, 'rb') as f:
                data = f.read()
            f.close()

            return data
        except:
            raise NeokamiParametersException('Invalid file format, file can not be read.')

    def sendFeedBack(self):
        '''
        Send label and image as feedback
        :return NeokamiResponse:
        '''
        self.checkHasAllParameters(['file'])
        self.check_base64()
        response = NeokamiHttpClient.post(
            self.getUrl('/feedback/image'),
            self.getApiKey(),
            {
                'data':self.getFile(),
                'label': self.getLabel(),
                'type': self.getFeedbackType(),
                'wait': self.getWait(),
                'max_retries': self.getMaxRetries(),
                'sleep': self.getSleep(),
                'sdk_version': self.SDK_VERSION,
                'sdk_lang': self.SDK_LANG
            }
        )

        return NeokamiResponse(response, self.getOutputFormat(), self.getSilentFails())

    def check_base64(self):
        '''
        Check if the file set has to be base64 encoded
        '''
        if(self.feedbackType == 'base64'):
            with open(self.file) as image_file:
                encoded_string = base64.b64encode(image_file.read())
                self.setFile(encoded_string)

    def getFile(self):
        '''
        Get the file's path
        :return string file:
        '''

        if hasattr(self, 'file'):
            return self.file
        else:
            raise NeokamiParametersException('File not set')


    def getStream(self):
        '''
        Get the bytestream
        :return bytestream stream:
        '''
        if hasattr(self, 'stream'):
            return self.stream
        else:
            raise NeokamiParametersException('Stream not set')


    def setFile(self, file):
        '''
        Set file's path
        :param string file:
        :return self:
        '''
        self.file = file
        return self


    def setStream(self, stream):
        '''
        Set bytestream
        :param bytestream stream:
        :return self:
        '''

        if isinstance(stream, bytes):
            self.stream = stream
            return self
        else:
            raise NeokamiParametersException('The stream set is not valid.')


    def getType(self):
        '''
        Get the classification type
        :return: string
        '''
        return self.type

    def setType(self, type):
        '''
        Set the classification type
        :param type:
        :return:
        '''
        self.type = type
        return self

    def getModel(self):
        '''
        Get the model name
        :return:
        '''

        return self.model

    def setModel(self, modelName):
        '''
        Set the model name
        :param modelName:
        :return self:
        '''

        self.model = modelName
        return self

    def getLabel(self):
        '''
        Get the image label
        :return:
        '''
        return self.label


    def setLabel(self, label):
        '''
        Set the image label
        :param label:
        :return self:
        '''

        self.label = label
        return self

    def getFeedbackType(self):
        '''
        Get feedback image type
        :return:
        '''
        return self.feedbackType

    def setFeedbackType(self, type):
        '''
        Set feedback image type
        :param type:
        :return self:
        '''
        self.feedbackType = type
        return self