"""

"""

from PIL import Image

def imageToBuffer(image, buffer_size, offset=(0,0)):
  """
  """
  if type(image) != Image.Image:
    raise TypeError("image must be a PIL Image object")

  offset_x, offset_y = offset
  buffer_x, buffer_y = buffer_size

  if (offset_x == offset_y == 0) and image.size == (buffer_x, buffer_size):
    # Received an 8x8 image with no offset, simply display it:
    return list(image.getdata())

  else:
    # Image needs cropping and/or growing
    # Make a copy so edits don't affect the original:
    img_copy = image.copy()
 
    if img_copy.size[0] >= (buffer_x + offset_x) and \
         img_copy.size[1] >= (buffer_y + offset_y):
      # the offset area fits within the image, only need to crop:
      buf = img_copy.crop((offset_x, offset_y, 
                           buffer_x+offset_x , buffer_y+offset_y)).getdata()
      return list(buf)

    else:
      # The offset 8x8 area runs off the edge of the image, need to
      # add new pixels
      if offset_x >= img_copy.size[0] or \
           offset_y >= img_copy.size[1]:
        # The area is completely outside of the image, nothing to display
        return [0]*buffer_x*buffer_y

      else:
        # Offset area not completely off the image, create a new image that
        # includes the extra pixels
        new_image = Image.new("1", (8, 8))

        crop_width_x = min(buffer_x+offset_x, img_copy.width-1)
        crop_width_y = min(buffer_y+offset_y, img_copy.height-1)
        cropped = img_copy.crop((offset_x, offset_y,
                                 crop_width_x, crop_width_y))

        new_image.paste(cropped, (0,0))
        return list(new_image.getdata())