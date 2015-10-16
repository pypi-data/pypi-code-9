from PIL import Image

def fit_image(img_path, max_width, max_height, save_to=None, filter=Image.ANTIALIAS):
    """ Resizes image and saves it to the specified location. If the image is
    smaller then the specified dimentions it will not be resized.
    
    If save_to is omitted or is the same as img_path, the original image will be overritten.
    
    File format will be automatically determined by extention.
    
    Returns file size of the new image.
    """
    
    img = Image.open(img_path)
    
    if not save_to:
        save_to = img_path
        
    ratio = 1.0 # defaults to horizontal ratio
    vratio = 1.0
    
    if img.size[0] > max_width:
        ratio = (max_width + 0.0)/img.size[0]
    if img.size[1] > max_height:
        vratio = (max_height + 0.0)/img.size[1]
    if ratio > vratio:
        ratio = vratio
    
    if ratio >= 1.0: # got image of smaller or equal size
        if save_to == img_path:
            return img.size # do nothing
        new_img = img.copy() # make a copy to save later
    else:
        size = int(img.size[0] * ratio), int(img.size[1] * ratio)
        new_img = img.resize(size, filter)
    new_img.save(save_to)
    return new_img.size
