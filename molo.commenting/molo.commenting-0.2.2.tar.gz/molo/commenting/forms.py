from django import forms
from django_comments.forms import CommentForm
from django.utils.translation import ugettext_lazy as _

from molo.commenting.models import MoloComment


class MoloCommentForm(CommentForm):
    email = forms.EmailField(label=_("Email address"), required=False)
    parent = forms.ModelChoiceField(
        queryset=MoloComment.objects.all(),
        required=False, widget=forms.HiddenInput)

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return MoloComment

    def get_comment_create_data(self):
        # Use the data of the superclass, and add in the parent field field
        data = super(MoloCommentForm, self).get_comment_create_data()
        data['parent'] = self.cleaned_data['parent']
        return data
