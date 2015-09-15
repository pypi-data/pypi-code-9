''' Copyright 2015 Neokami GmbH. '''

#import NeokamiHttpClient
from .NeokamiRequest import NeokamiRequest
from .NeokamiResponse import NeokamiResponse
from .Exceptions.NeokamiParametersException import NeokamiParametersException
from .HttpClients.NeokamiCurl import NeokamiHttpClient

NeokamiHttpClient = NeokamiHttpClient()

class ImageAnalyser(NeokamiRequest):

    type = None

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

        response = NeokamiHttpClient.postBinary(
            self.getUrl('/analyse/image'),
            bytestream,
            self.getApiKey(),
            {
                'wait': self.getWait(),
                'max_retries': self.getMaxRetries(),
                'sleep': self.getSleep(),
                'type': self.getType(),
                'sdk_version': self.SDK_VERSION,
                'sdk_lang': self.SDK_LANG
            }
        )

        return NeokamiResponse(response, self.getOutputFormat(), self.getSilentFails())


    def analyseFromStream(self):
        '''
        Analyse image from bytestream
        :return object NeokamiResponse:
        '''

        bytestream = self.getStream()

        response = NeokamiHttpClient.postBinary(
            self.getUrl('/analyse/image'),
            bytestream,
            self.getApiKey(),
            {
                'wait': self.getWait(),
                'max_retries': self.getMaxRetries(),
                'sleep': self.getSleep(),
                'type': self.getType(),
                'sdk_version': self.SDK_VERSION,
                'sdk_lang': self.SDK_LANG
            }
        )
        return NeokamiResponse(response, self.getOutputFormat(), self.getSilentFails())


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
        :return: string
        '''
        return self.type

    def setType(self, type):
        '''
        :param type:
        :return:
        '''
        self.type = type
        return self
