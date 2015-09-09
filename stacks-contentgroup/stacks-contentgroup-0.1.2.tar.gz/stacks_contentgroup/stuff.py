from textplusstuff import registry

from .models import ContentGroup
from .serializers import ContentGroupSerializer


class ContentGroupStuff(registry.ModelStuff):
    queryset = ContentGroup.objects.prefetch_related('content_set')
    verbose_name = 'Content Group'
    verbose_name_plural = 'Content Groups'
    description = 'Display a Content Group'
    serializer_class = ContentGroupSerializer
    renditions = [
        registry.Rendition(
            short_name='3up',
            verbose_name='Content Group 3-Up',
            description='Displays the Content Group in stacks of three.',
            path_to_template='stacks_contentgroup/contentgroup/'
                             'contentgroup-3up.html',
            rendition_type='block',
        ),
        registry.Rendition(
            short_name='2up',
            verbose_name='Content Group 2-Up',
            description='Displays the Content Group in stacks of two.',
            path_to_template='stacks_contentgroup/contentgroup/'
                             'contentgroup-2up.html',
            rendition_type='block'
        )
    ]
    list_display = ('id', 'name')

registry.stuff_registry.add_modelstuff(
    ContentGroup,
    ContentGroupStuff,
    groups=['stacks', ]
)
