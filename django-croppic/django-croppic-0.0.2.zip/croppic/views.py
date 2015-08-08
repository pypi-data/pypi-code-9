import json
import StringIO

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse

from PIL import Image

from .models import Picture
from .forms import PicForm, CropForm
from .utils import validate_image_size, image_id_from_url
from .conf import MIN_SIZE_ERROR


def upload_pic(request):
    """Handel the initial upload of the image

    Return:
        Successful Upload:
            status (str): "success"
            url (str): the url of the image
            width (float): The width in pixels of the image
            Height (float): the height of the image in pixels
    """

    response_data = {'status': 'error', 'message': 'Bad request.'}

    if request.method == 'POST':
        form = PicForm(request.POST, {'image': request.FILES['img']})
        if form.is_valid():
            pic = form.save(commit=False)
            if request.user and request.user.is_authenticated():
                pic.user = request.user
            pic.save()
            with Image.open(pic.image) as original:
                width, height = original.size  # needed for croppic's zoom feature
                if validate_image_size(width, height):
                    response_data = {
                        'status': 'success',
                        'url': pic.image.url + '?image_id=%d' % pic.id,
                        'width': width,
                        'height': height,
                    }
                else:
                    response_data = {'status': 'error', 'message': MIN_SIZE_ERROR}
        else:
            response_data = {'status': 'error', 'message': 'Invalid image.'}

    # Croppic will parse the information returned into json. content_type needs
    # to be set as 'text/plain'
    return HttpResponse(json.dumps(response_data),
                        content_type="text/plain")


def crop_pic(request):
    """Handel the cropping of the Image

    POST
    ----
    data:
        imgUrl = forms.CharField(max_length=1000)   # your image path (the one we received after successful upload)
        imgInitW = forms.DecimalField() 	    # your image original width (the one we received after upload)
        imgInitH = forms.DecimalField()	            # your image original height (the one we received after upload)
        imgW = forms.DecimalField()		    # your new scaled image width
        imgH = forms.DecimalField()		    # your new scaled image height
        imgX1 = forms.DecimalField()		    # top left corner of the cropped image in relation to scaled image
        imgY1 = forms.DecimalField()		    # top left corner of the cropped image in relation to scaled image
        cropW = forms.DecimalField()		    # cropped image width
        cropH = forms.DecimalField()		    # cropped image height

    Returns:
        Successful upload:
            status (str): "success"
            url (str): the full url of the image
        Unsuccessful upload:
            status (str): "error"
            message (list-str): a list of the errors from the django model form
    """

    response_data = {'status': 'error', 'message': 'Bad request.'}

    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():

            # get the url of the working image i.e. www.example.com/media/pictures/uploaded_image.png
            image_url = form.cleaned_data['imgUrl']

            # get the image_id
            image_id = image_id_from_url(image_url)

            pic = Picture.objects.get(id=image_id)
            with Image.open(pic.image) as original:
                new_image = original.resize(
                    (form.cleaned_data['imgW'], form.cleaned_data['imgH']), Image.ANTIALIAS)

                x1 = form.cleaned_data['imgX1']
                y1 = form.cleaned_data['imgY1']
                x2 = form.cleaned_data['cropW'] + x1
                y2 = form.cleaned_data['cropH'] + y1
                new_image = new_image.crop((x1, y1, x2, y2))
                if validate_image_size(*new_image.size):
                    # Save the cropped image and replace the original image
                    crop_io = StringIO.StringIO()
                    try:
                        new_image.save(crop_io, original.format)

                        previous_file_path = pic.image.name
                        filename = previous_file_path.rsplit('/')[-1]
                        pic.image.save(filename, ContentFile(crop_io.getvalue()))
                    finally:
                        crop_io.close()

                    # delete previous file
                    try:
                        default_storage.delete(previous_file_path)
                    except OSError:
                        pass

                    response_data = {
                        'status': 'success',
                        'url': pic.image.url + '?image_id=%d' % pic.id,
                    }
                else:
                    response_data = {'status': 'error', 'message': MIN_SIZE_ERROR}
        else:
            response_data = {'status': 'error', 'message': 'Image cropping failed.'}

    # Croppic will parse the information returned into json. content_type needs
    # to be set as 'text/plain'
    return HttpResponse(json.dumps(response_data),
                        content_type='text/plain')
