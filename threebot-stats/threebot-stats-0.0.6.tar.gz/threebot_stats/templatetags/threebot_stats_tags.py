from django import template

from threebot_stats.utils import *

register = template.Library()

@register.assignment_tag
def avg_response_time(workflow):
   return average_response_time(workflow)