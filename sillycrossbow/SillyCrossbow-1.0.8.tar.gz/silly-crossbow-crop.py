# encoding: utf8
import sys
from PIL import Image
from SillyCrossbow import CropTransparent, SillyCrossbow, crop_image

if len(sys.argv) < 3:
    raise SystemExit('''
Usage: python silly-crossbow-crop.py <path-to-rgba-png> <threshold>
Example: python silly-crossbow-crop.py data/fire.png 50
''')

print SillyCrossbow()

fire = Image.open(sys.argv[1])
fire.show()
cropper = CropTransparent(fire.width, fire.height, int(sys.argv[2]), fire.tostring(), True)

print cropper.getCroppedOffsetX()
print cropper.getCroppedOffsetY()
print cropper.getCroppedHeight()
print cropper.getCroppedWidth()

crop_rect = cropper.getRect()

print crop_rect.x
print crop_rect.y
print crop_rect.width
print crop_rect.height

cropped_image, x, y, w, h = crop_image(fire, 50)
cropped_image.show()

# crim2 = cropper.getCroppedImage()
# crim3 = Image.frombytes(mode='RGBA',
#                         size=(crim2.getWidth(), crim2.getHeight()),
#                         data=str(crim2.getData()))
# crim3.show()