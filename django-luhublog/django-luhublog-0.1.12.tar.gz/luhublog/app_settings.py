from django.conf import settings

SEARCH_FIELDS = getattr(settings, 'BLOG_SEARCH_FIELDS',
                        ['title', 'lead', 'content',
                         'excerpt', 'image_caption', 'tags'])

TEST = "esto es un test"