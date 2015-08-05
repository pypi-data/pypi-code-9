from django import template
register = template.Library()


@register.assignment_tag
def get_random_question(section, quiz_random, user):
    return quiz_random.get_random_question(section, quiz_random, user)
