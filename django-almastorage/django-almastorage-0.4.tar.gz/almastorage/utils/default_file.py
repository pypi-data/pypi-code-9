import os
from almastorage.models import SwiftFile, DEFAULT_CONTAINER_TITLE
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned 
from django.conf import settings

FOLDER_PATH = 'img/'
        
def set_file(filename, content_type, folder_path = FOLDER_PATH, container_title = DEFAULT_CONTAINER_TITLE):
    try:
        swiftfile = SwiftFile.objects.get(filename=filename)
    except MultipleObjectsReturned:
        swiftfile = SwiftFile.objects.filter(filename=filename).first()
    except ObjectDoesNotExist:
        file_path = os.path.join(settings.BASE_DIR + settings.STATIC_URL + folder_path + filename)
        swiftfile = SwiftFile.upload_file(file_contents=open(file_path, "rb").read(), filename=filename, content_type=content_type, container_title=container_title)

    return swiftfile