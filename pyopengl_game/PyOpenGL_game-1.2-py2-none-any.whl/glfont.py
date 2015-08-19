from PIL import Image, ImageDraw, ImageFont
from numpy import *


def load_font(filename, size):
    '''
    Load TrueType font from file
    @param filename: name of file
    @param size: size of characters
    @return: font
    '''
    return ImageFont.truetype(filename, size)


def render_text(font, text, color, size):
    '''
    Render text to image
    @param font: font
    @param text: text
    @param color: text color
    @param size: size of characters
    @return: tuple: (height, width, image data)
    '''
    sz = font.getsize(text)[0], size
    img = Image.new("RGBA", sz, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, color, font=font)
    return sz[0], sz[1], concatenate(img.getdata())
