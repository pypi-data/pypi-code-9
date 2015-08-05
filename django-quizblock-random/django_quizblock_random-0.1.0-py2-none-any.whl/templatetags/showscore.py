from django import template
register = template.Library()


@register.assignment_tag
def get_questions(section, block, question, user):
    block.get_random_question_set(section, block, question, user)
    is_correct = question.is_user_correct(user)
    return is_correct
