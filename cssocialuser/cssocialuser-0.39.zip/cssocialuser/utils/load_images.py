from photologue.models import Photo
from urllib2 import urlopen
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile

from cssocialuser.utils.slug import time_slug, time_slug_long, time_slug_string


from random import  randint

from cStringIO import StringIO
try:
    from PIL import Image
except ImportError:
    import Image


def _getUrlImage(url):
    """ """
    try:
        socket = urlopen(url)
    except:
        socket = None
    return socket 


def loadUrlImage(url='', title='', tags='', format='jpg', slug=''):
    """ """
    if not url:
        url = 'http://irudiak.argazkiak.org/1d3023545b4051907e533648e66329f8_c.jpg'
        title = 'Kakalardoa'
        tags = 'test argazkiak'

    if not slug:
        slug = time_slug()

    if Photo.objects.filter(title_slug=slug):
        slug = time_slug_long()

    title = title[:99]
    if Photo.objects.filter(title=title):
        title = '%s %s' % (slug, title)[:90]
    
        
    image = _getUrlImage(url)

    if not image:
        return 0

    photo = Photo()
    photo.title = title[:100]
    photo.tags = tags
    photo.title_slug = slug
    
    try:
        image_t = Image.open(ContentFile(image.read()))
        image_t = image_t.convert("RGB")
        f=StringIO()
        image_t.save(f,"JPEG")
        f.seek(0)    
    
        photo.image.save('%s.%s' % (slug,format), ContentFile(f.read()))

    except Exception, e:
        print 'Errorea irudi honekin RGB', photo.title_slug, e
        return photo      

    try:
        photo.save()
    except:
        print 'Errorea irudi honekin', photo.title_slug

    return photo
    
    
def handle_uploaded_file(f,title):
    """ """
    photo = Photo()
    photo.title = u'%s %s' % (time_slug_string(), title) 
    photo.title_slug = time_slug_string()
    photo.image = f
    photo.save()
    return photo    
    