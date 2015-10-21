import clr
clr.AddReferenceToFileAndPath("DDIY.dll")
clr.AddReference("System.Drawing")
import gc

import DDIY
from System.Drawing import Image

class ImageMatcher:
    """ Looks for template image in source image. """
    def __init__(self):
        self._imagematcher = DDIY.ImageMatcher()

    def __repr__(self):
        return "<DDIY.ImageMatcher wrapper>"

    def SetThreshold(self, threshold):
        """ Sets minimal color similarity between template and source.
            1.0 means 100% same colors. Higher value also means quicker searching.
            Range 0.0 -> 1.0
        """
        self.SetThreshold(threshold)

    def CropImage(self, image, rectangle):
        """ Crops image using rectangle. """
        return self._imagematcher.CropImage(image, rectangle)

    def FindTemplate(self, sourceImage, templateImage, sourceRectangle=None):
        """ Expects:
                System.Drawing.Image as sourceImage
                System.Drawing.Image or string(path) as templateImage
                System.Drawing.Rectangle as sourceRectangle
            Returns rectangle(position and size). Compare with System.Drawing.Rectangle.Empty!
        """
        fromFile = False
        if not isinstance(templateImage, Image):
            templateImage = Image.FromFile(templateImage)
            fromFile = True

        rectangle = None
        if sourceRectangle:
            rectangle = self._imagematcher.FindTemplate(sourceImage, templateImage, sourceRectangle)
        else:
            rectangle = self._imagematcher.FindTemplate(sourceImage, templateImage)

        if fromFile:
            templateImage.Dispose()

        gc.collect()
        return rectangle
