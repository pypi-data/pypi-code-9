from textplusstuff import registry

from .models import Tweet
from .serializers import TweetSerializer


class StacksTweetStuff(registry.ModelStuff):
    queryset = Tweet.objects.all()

    description = 'A tweet.'
    serializer_class = TweetSerializer
    renditions = [
        registry.Rendition(
            short_name='full_width',
            verbose_name="Full Width Tweet",
            description="An tweet that spans the full width of the page.",
            path_to_template='stacks_twitter/tweet/'
                             'tweet-full_width.html'
        ),
    ]
    # The attributes used in the list (table) display of the front-end
    # editing tool.
    list_display = ('id', 'user', 'text')


registry.stuff_registry.add_modelstuff(
    Tweet,
    StacksTweetStuff,
    groups=['stacks']
)
