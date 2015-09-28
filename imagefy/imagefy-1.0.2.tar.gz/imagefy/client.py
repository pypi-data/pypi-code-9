import json
import requests

from requests.exceptions import RequestException

from imagefy.exceptions import ImagefyOperationException

from imagefy.models import Image, ModifiedImage

def check_tags(tags):
    """
    Tags parser for Imagefy API. Takes an iterable list as an argument and produces
    a string with the tags separated with colons.
    :param tags: The tags list.
    """
    if tags is not None:
        return ', '.join(tags)
    else:
        raise ValueError('Invalid tag list.')


class Imagefy(object):

    """
    Main Imagefy client.
    """

    def __init__(self, host, api_key=None):
        """
        Create a new connection to Imagefy.
        :param host: Imagefy server address (and port).
        :param api_key: The API key used for authentication.
        """
        self.host = host
        self.api_key = api_key

        if not host:
            raise TypeError('You have to specify the host.')

        if not api_key:
            raise TypeError('You have to specify the API key.')

    def upload(self, source_image, tags=None):
        """
        Uploads an image to the Imagefy server using the POST method.
        If successful, returns 201 CREATED with an instance saved image.
        :param source_image: The image to be sent.
        :param tags: Optional image tags.
        :return: an instance of the saved image.
        """

        url = self.host
        headers = {
            'Authorization': 'Token %s' % self.api_key
        }

        try:
            image = open(source_image.name, 'rb')
        except IOError as e:
            raise ImagefyOperationException("Couldn't open file.", 'file_open', original_exc=e)

        files = {
            'image': image
        }
        data = {}
        if tags:
            data['tags'] = check_tags(tags)

        try:
            response = requests.post(url=url, headers=headers, data=data, files=files)
            if response.status_code == 201:
                data = response.json()
                return Image(data['id'], data['image'], data['created'],
                             data['format'], data['width'], data['height'],
                             data['user'], data['tags'])
        except RequestException as e:
            raise ImagefyOperationException("Network error.", 'upload', original_exc=e)
        finally:
            # Close the file
            try:
                image.close()
            except IOError:
                pass

    def modify(self, uuid, actions):
        """
        Used to request modified images of the original image.
        :param args:
        :param kwargs:
        :return:
        """
        url = '%s%s/modified/' % (self.host, uuid)
        headers = {
            'Authorization': 'Token %s' % self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            actions = json.dumps(actions)
            response = requests.post(url, headers=headers, data=actions)
            if response.status_code == 201:
                data = response.json()
                return ModifiedImage(data['id'], data['image'], data['created'],
                                     data['format'], data['width'], data['height'],
                                     data['source'], data['actions'], data['actions_hash'])
        except RequestException as e:
            raise ImagefyOperationException("Network error.", 'modification', original_exc=e)

    def retrieve(self, uuid, modified=None):
        """
        Fetches an image from the Imagefy API.
        :param uuid: An UUID of the (original) image.
        :param modified: An optional UUID for the modified version of the image.
        """
        url = '%s%s/' % (self.host, uuid)
        if modified is not None:
            url += 'modified/%s/' % modified
        headers = {
            'Authorization': 'Token %s' % self.api_key
        }

        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if modified is not None:
                    return ModifiedImage(data['id'], data['image'], data['created'],
                                         data['format'], data['width'], data['height'],
                                         data['source'], data['actions'], data['actions_hash'])
                return Image(data['id'], data['image'], data['created'],
                             data['format'], data['width'], data['height'],
                             data['user'], data['tags'])
        except RequestException as e:
            raise ImagefyOperationException("Network error.", 'retrieval', original_exc=e)

    def retrieve_metadata(self, uuid):
        """
        Fetches an image's metadata from the Imagefy API.
        :param uuid: An UUID of the image.
        """
        url = '%s%s/meta/' % (self.host, uuid)
        headers = {
            'Authorization': 'Token %s' % self.api_key
        }

        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data
        except RequestException as e:
            raise ImagefyOperationException("Network error.", 'metadata', original_exc=e)

    def delete(self, uuid):
        """
        Deletes an uploaded image (and its modified images)
        from the Imagefy API.
        :param uuid: An UUID of the image.
        """
        url = '%s%s/' % (self.host, uuid)
        headers = {
            'Authorization': 'Token %s' % self.api_key
        }

        try:
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 204:
                return True
        except RequestException as e:
            raise ImagefyOperationException("Network error.", 'deletion', original_exc=e)
