from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Still need to deal with access control to these files using this
# storage system.  Likely move this class out to another file
# that handles viewing these files and the permissions they recieve


class ApplicationStorage(FileSystemStorage):
    """
       Does file replacement on file fields instead of renaming them
    """

    def __init__(self, location=None, base_url=None):
        if location is None:
            self.location = settings.APP_STORAGE_ROOT
        if base_url is None:
            # This app could be run from any url, grab the url from the
            # base view.
            self.base_url = "%sstorage/" % settings.APP_STORAGE_URL
        super(ApplicationStorage, self).__init__(location=self.location,
                                                 base_url=self.base_url)
        
    
    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            self.delete(name)
        return name

def upload_to_path(instance, filename):
    # Save the instance to get the ID
    return "%s/%s/%s/%s" % ( instance.app.app_definition.slug,
                                instance.app.id, instance.field_def.slug,
                                filename)

