from base64 import b64decode
from six import string_types
from ._base import Module, extract_value


class File(Module):
    _name = 'file'

    @extract_value()
    def upload(self, file, return_content=None, context=None):
        """Upload a file for use in import functions.

        :param file: file-like object open for reading
        :param return_content: whether to return the uploaded data as part of the response
        :return: random name assigned to file
        """

        r = self._request('upload', {
            'returnContent': return_content,
            'context': context
        }, file)
        r['_key'] = None if return_content or context else 'filename'
        return r

    def name_or_upload(self, data):
        """If data is a string, assume it's a filename and return it;
        otherwise assume it's a file, upload it, and return the generated filename.

        This is useful inside import functions to allow new and existing files.

        :param data: filename or file-like object to upload
        :return: filename
        """

        return data if isinstance(data, string_types) else self.upload(data, False)

    @extract_value('filename')
    def clear(self, name):
        """Delete a file previously uploaded.

        :param name: name of file returned after upload
        :return: path of deleted file
        """

        return self._request('clear', {
            'filename': name
        })

    def get_image(self, type, id, sequence=None):
        return b64decode(self._request('getImage', {
            'imageType': type,
            'objectID': id,
            'sequence': sequence
        })['image'])
