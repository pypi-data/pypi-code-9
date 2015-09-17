from django.contrib import admin

from textplusstuff.admin import TextPlusStuffRegisteredModelAdmin

from .models import Tweet
from .forms import (
    TweetEditForm,
    TweetCreateForm
)


class TweetAdmin(TextPlusStuffRegisteredModelAdmin):
    form = TweetEditForm
    add_form = TweetCreateForm
    readonly_fields = ('user', 'hashtags', 'tweet_link')
    fieldsets = (
        (None, {
            'fields': ('tweet_link',)
        }),
        ('Tweet Metadata', {
            'fields': (
                'user',
                'text',
                'hashtags'
            )
        })
    )
    add_fieldsets = (
        (None, {
            'fields': ('tweet_id',)
        }),
    )
    list_display = ['text', 'user', 'tweet_id']
    search_fields = ['text', 'user__username']

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(TweetAdmin, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during video creation
        """
        defaults = {}
        if obj is None:
            kwargs.update({
                'form': self.add_form,
                'fields': admin.utils.flatten_fieldsets(self.add_fieldsets),
            })
        defaults.update(kwargs)
        return super(TweetAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Tweet, TweetAdmin)
