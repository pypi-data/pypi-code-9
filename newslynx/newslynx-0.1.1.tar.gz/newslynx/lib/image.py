import cStringIO
import base64
import mimetypes
from urlparse import urljoin

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageOps

from newslynx.lib import network
from newslynx.lib import url
from newslynx import settings
from newslynx.util import uniq

IMG_TAGS = [('img', 'src'), ('a', 'href')]


def b64_thumbnail_from_url(img_url, **kw):
    """
    Download an image and create a base64 thumbnail.
    """
    if not img_url:
        return None

    size = kw.get('size', settings.THUMBNAIL_SIZE)
    default_fmt = kw.get('format', settings.THUMBNAIL_DEFAULT_FORMAT)
    fmt = None

    # override fmt with default fmt
    fmt = url.get_filetype(img_url)

    # get the image
    resp = get_url(img_url)
    if not resp:
        return None
    data, mime_fmt = resp

    # override fmt with format from mimetype
    if not fmt:
        fmt = mime_fmt

    # if we still don't have a format, fall back on default
    if not fmt:
        fmt = default_fmt

    # PIL doesn't like JPG
    if fmt.lower() == 'jpg':
        fmt = "jpeg"

    # turn into Pillow object
    file = cStringIO.StringIO(data)

    # if this fails then it's not an image.
    try:
        image = Image.open(file)

        # fit to a thumbnail
        thumb = ImageOps.fit(image, size, Image.ANTIALIAS)
    except:
        return None

    # convert to base64
    img_buffer = cStringIO.StringIO()
    thumb.save(img_buffer, format=fmt)
    img_str = base64.b64encode(img_buffer.getvalue())

    # format + return
    return "data:image/{};base64,{}".format(fmt, img_str)


@network.retry(attempts=2)
def get_url(img_url):
    """
    Fetch an image and detect its filetype
    """
    fmt = None
    r = requests.get(img_url, **network.get_request_kwargs())
    mimetype = r.headers.get('content-type', None)
    if mimetype:
        fmt = extension_from_mimetype(mimetype)
    return r.content, fmt


def extension_from_mimetype(mimetype):
    """
    Guess a image's extension from it's mimetype.
    """
    ext = mimetypes.guess_extension(mimetype)
    if ext.startswith('.'):
        ext = ext[1:]
    # this is a bug in mimetypes
    if ext == 'jpe':
        return 'jpeg'
    return ext


def from_html(htmlstring, source=None):
    """
    Extract all img urls from an html string
    """
    if not htmlstring:
        return []
    soup = BeautifulSoup(htmlstring)
    out_imgs = []

    for tag, attr in IMG_TAGS:

        for el in soup.find_all(tag):

            img_url = el.attrs.get(attr)
            if not img_url:
                continue

            # only take images with known formats
            fmt = url.is_image(img_url)
            if not fmt:
                continue

            if img_url.startswith('//:'):
                img_url = "http{}".format(img_url)

            # absolutify images if we know their source.
            if img_url.startswith('/') or not img_url.startswith('http'):
                if source:
                    img_url = urljoin(source, img_url)
                else:
                    continue

            out_imgs.append(img_url)
    return uniq(out_imgs)
