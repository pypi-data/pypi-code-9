from django import template
from ..models.facebook import Facebook
from ..models.twitter import Twitter
from ..models.linkedin import Linkedin

register = template.Library()

class NOT_PROVIDED: pass

@register.inclusion_tag('fibanez_social/social_links.html')
def display_social_nav():
    """
    Display Facebook, Twitter or Linkdin buttons
    """
    return {'facebook_link': Facebook.objects.order_by('-id')[0] if Facebook.objects.exists() else [],
            'twitter_link': Twitter.objects.order_by('-id')[0] if Twitter.objects.exists() else [],
            'linkedin_link': Linkedin.objects.order_by('-id')[0] if Linkedin.objects.exists() else [],
            }
