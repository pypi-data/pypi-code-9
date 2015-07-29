# encoding: utf8
from PIL import Image
from SillyCrossbow import CropTransparent


def crop_image(image, threshold):
    cropper = CropTransparent(image.width, image.height, threshold, image.tostring())
    x = cropper.getCroppedOffsetX()
    y = cropper.getCroppedOffsetY()
    width = cropper.getCroppedWidth()
    height = cropper.getCroppedHeight()

    cropped_image = image.crop((x, y, x + width, y + height))

    return cropped_image, x, y, width, height


def crop_image_from_file(filename, threshold):
    return crop_image(Image.open(filename), threshold)


def crop_image2(image, threshold):
    cropper = CropTransparent(image.width, image.height, threshold, image.tostring(), True)
    x = cropper.getCroppedOffsetX()
    y = cropper.getCroppedOffsetY()
    width = cropper.getCroppedWidth()
    height = cropper.getCroppedHeight()
    image = cropper.getCroppedImage()

    return image, x, y, width, height


def crop_image2_from_file(filename, threshold):
    return crop_image2(Image.open(filename), threshold)


