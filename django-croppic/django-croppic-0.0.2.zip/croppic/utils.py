import urlparse

from .conf import MIN_SIZE


def validate_image_size(width, height):
    """
    Validate if image size is according to MIN_SIZE (if defined)
    :param width: Width of an Image
    :param height: Height of an Image
    :return: Boolean
    """
    valid = True
    if MIN_SIZE is not None:
        min_width, min_height = MIN_SIZE
        if width < min_width or height < min_height:
            valid = False
    return valid


def image_id_from_url(url):
    """
    Get Image id (primary key of models.Picture from URL)
    :param url: Uploaded image url
    :return: image_id or None
    """
    parsed = urlparse.urlparse(url)
    image_id = urlparse.parse_qs(parsed.query).get('image_id')
    if image_id:
        image_id = image_id[0]
    return image_id
