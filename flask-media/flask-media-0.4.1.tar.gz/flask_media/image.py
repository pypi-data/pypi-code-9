# coding: utf-8
import StringIO
import os
from werkzeug.datastructures import FileStorage

try:
    from PIL import Image, ImageOps, ImageChops
except ImportError:
    raise RuntimeError('Package Pillow not installed!')

__all__ = (
    'thumbnail',
    'crop_image'
)

__author__ = 'vadim'


def _create_name(name, ext, *args):
    args_name = '_'.join(['%s' % v for v in args if v])
    return name + '_' + args_name + ext


def thumbnail(img_path, size, crop=None, thumb_path=None):
    """
    :param img_path: path to original file
    :param size: size return thumb - '100x100'
    :param crop: crop return thumb - 'fit', 'pad' or None
    :param thumb_path: path save thumbnail
    :return: :thumb_url:
    """
    width, height = [int(x) for x in size.split('x')]
    orig_path, orig_name = os.path.split(img_path)
    name, ext = os.path.splitext(orig_name)

    miniature = _create_name(name, ext, size, crop)

    thumb_filename = os.path.join(thumb_path, miniature)

    if not os.path.exists(thumb_filename):
        if not os.path.exists(thumb_path):
            os.makedirs(thumb_path)
        try:
            image = Image.open(img_path)

            if crop == 'fit':
                img = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
            else:
                img = image.copy()
                img.thumbnail((width, height), Image.ANTIALIAS)

                if crop == 'pad':
                    image_size = img.size
                    img = img.crop((0, 0, width, height))
                    offset_x = max((width - image_size[0]) / 2, 0)
                    offset_y = max((height - image_size[1]) / 2, 0)
                    img = ImageChops.offset(img, offset_x, offset_y)

            img.save(thumb_filename, image.format)
        except IOError:
            return None

    return thumb_filename


def crop_image(storage, left, upper, right, lower):
    io = StringIO.StringIO()
    image = Image.open(storage)
    image_format = image.format
    image = image.crop((left, upper, right, lower))
    image.save(io, format=image_format)
    image_file = FileStorage(io, storage.filename, storage.name, storage.content_type, io.len, storage.headers)
    image_file.seek(0)
    return image_file