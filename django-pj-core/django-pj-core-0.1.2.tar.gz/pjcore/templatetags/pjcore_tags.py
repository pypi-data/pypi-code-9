# Std libraries
from django import template

register = template.Library()

PERCENTAGE_DEFAULT_CLASSES = {
    'negative': 'negative',
    'positive': 'positive'
}

@register.filter()
def colorize_percentage(value):
    """
    Colorizes value depending on if it is less (default color red) or more
    (default color green) than zero. Indented usage in determining what
    direction certain stock value changes during a day (hence the
    _percentage postfix) 
    
    Example:

       {{ data.change|colorize_percentage }}

    :param value: (percentage) value based on which colorizing is done
    :type value: decimal.Decimal (or any that can be compared to 0)
    :return: color name to be used as css class
    :rtype: string
    """
    
    if value >= 0:
        return PERCENTAGE_DEFAULT_CLASSES['positive']
    else:
        return PERCENTAGE_DEFAULT_CLASSES['negative']

