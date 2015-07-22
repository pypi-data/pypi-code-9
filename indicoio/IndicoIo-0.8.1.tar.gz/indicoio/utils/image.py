"""
Image Utils
Handles preprocessing images before they are sent to the server
"""
import os.path, base64, StringIO, re, warnings

from PIL import Image

from indicoio.utils.errors import IndicoError, DataStructureException

B64_PATTERN = re.compile("^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)")

def image_preprocess(image, size=(48,48), batch=False):
    """
    Takes an image and prepares it for sending to the api including
    resizing and image data/structure standardizing.
    """
    if batch:
        return [image_preprocess(img, batch=False) for img in image]

    if isinstance(image, basestring):
        b64_str = re.sub('^data:image/.+;base64,', '', image)
        if os.path.isfile(image):
            # check type of element
            out_image = Image.open(image)
        elif B64_PATTERN.match(b64_str) is not None:
            return b64_str
        else:
            raise IndicoError("Snose tring provided must be a valid filepath or base64 encoded string")

    elif isinstance(image, list): # image passed in is a list and not np.array
        warnings.warn(
            "Input as lists of pixels will be deprecated in the next major update",
            DeprecationWarning
        )
        out_image = process_list_image(image)
    elif isinstance(image, Image.Image):
        out_image = image
    elif type(image).__name__ == "ndarray": # image is from numpy/scipy
        if "float" in str(image.dtype) and image.min() >= 0 and image.max() <= 1:
            image *= 255.
        try:
            out_image = Image.fromarray(image.astype("uint8"))
        except TypeError as e:
            raise IndicoError("Please ensure the numpy array is acceptable by PIL. Values must be between 0 and 1 or between 0 and 255 in greyscale, rgb, or rgba format.")

    else:
        raise IndicoError("Image must be a filepath, base64 encoded string, or a numpy array")

    # image resizing
    if size:
        out_image = out_image.resize(size)

    # convert to base64
    temp_output = StringIO.StringIO()
    out_image.save(temp_output, format='PNG')
    temp_output.seek(0)
    output_s = temp_output.read()

    return base64.b64encode(output_s)


def get_list_dimensions(_list):
    """
    Takes a nested list and returns the size of each dimension followed
    by the element type in the list
    """
    if isinstance(_list, list) or isinstance(_list, tuple):
        return [len(_list)] + get_list_dimensions(_list[0])
    return []


def get_element_type(_list, dimens):
    """
    Given the dimensions of a nested list and the list, returns the type of the
    elements in the inner list.
    """
    elem = _list
    for _ in xrange(len(dimens)):
        elem = elem[0]
    return type(elem)


def process_list_image(_list):
    """
    Processes list to be [[(int, int, int), ...]]
    """
    # Check if list is empty
    if not _list:
        return _list

    dimens = get_list_dimensions(_list)
    data_type = get_element_type(_list, dimens)

    seq_obj = []

    out_image = Image.new("RGB", (dimens[0], dimens[1]))
    for i in xrange(dimens[0]):
        for j in xrange(dimens[1]):
            elem = _list[i][j]
            if len(dimens) >= 3:
                #RGB(A)
                if data_type == float:
                    seq_obj.append((int(elem[0] * 255), int(elem[1] * 255), int(elem[2] * 255)))
                else:
                    seq_obj.append(tuple(elem[0:3]))
            elif data_type == float:
                #Grayscale 0 - 1.0f
                seq_obj.append((int(elem * 255), ) * 3)
            else:
                #Grayscale 0 - 255
                seq_obj.append((elem, ) * 3)

    #Needs to be 0 - 255 in flattened list of (R, G, B)
    out_image.putdata(data = seq_obj)

    return out_image
