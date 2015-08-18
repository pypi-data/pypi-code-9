from aniso8601 import parse_datetime

class Image(object):
    def __init__(self, uuid, image, created, user=None, tags=None):
        """
        A class representing an image object returned from the Imagefy API.
        :param uuid: The image's UUID, used to fetch modified versions of the image.
        :param url: The url from which the original file can be retrieved.
        :param created: The time and date for the image upload.
        :param tags: Optional list of tags.
        :return: An image instance.
        """
        self.uuid = uuid
        self.image = image
        self.created = parse_datetime(created)
        self.user = user
        self.tags = tags


class ModifiedImage(object):
    def __init__(self, uuid, image, created, source, settings):
        """
        A class representing a modified image returned from the Imagefy API.
        :param uuid: The modified image's UUID.
        :param image: The url from which the modified image can be retrieved.
        :param created: The time and date for the image upload.
        :param source: The original image's url.
        :param settings: The settings used to modify the original image.
        :return: A modified image instance.
        """
        self.uuid = uuid
        self.image = image
        self.created = parse_datetime(created)
        self.source = source
        self.settings = settings
