try:
    from PIL import Image
except ImportError:
    import Image

from django.conf import settings
from django.http import HttpResponse
from django.views.generic.base import TemplateView


from .models import *

class TrackView(TemplateView):
    

    def render_to_response(self, context, **response_kwargs):  

      try:
        tracking_categories = settings.TRACKING_CATEGORIES
      except:
        tracking_categories = []

      category = self.request.GET.get('category', None)
      if category in tracking_categories:

        full_url = self.request.GET.get('url', None)
        action = self.request.GET.get('action', None)
        label = self.request.GET.get('label', None)
        value = self.request.GET.get('value', None)
        value = None if not value else float(value)
        content = self.request.GET.get('content', None)
        ua = self.request.META['HTTP_USER_AGENT']

        # print 'full_url: %s'%(full_url)
        # print 'category: %s'%(category)
        # print 'action: %s'%(action)
        # print 'label: %s'%(label)
        # print 'value: %s'%(value)
        # print 'content: %s'%(content)
        # print 'ua: %s'%(ua)

        Event.track(full_url, category, action, label, value, content, ua)

      return output_spaceball_image()

def output_spaceball_image():

    img = Image.new("RGB", (1,1), "#ffffff")

    response = HttpResponse(content_type="image/jpeg")

    img.save(response, "JPEG")

    #NEVER CACHE
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response