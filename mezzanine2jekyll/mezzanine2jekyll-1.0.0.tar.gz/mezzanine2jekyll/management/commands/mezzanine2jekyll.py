from django.core.management.base import BaseCommand
from mezzanine.blog.models import BlogPost
import os
import re

class Command(BaseCommand):
    help = 'Export Mezzanine blog posts as Jekyll files'

    def add_arguments(self, parser):
        parser.add_argument('output_dir', help='Where to put the outputted Jekyll files')

    def handle(self, *args, **options):
        for post in BlogPost.objects.all():
            header = {
                'layout': 'post',
                'title': post.title.replace(':', ''),
                'date': post.publish_date,
                'categories': ' '.join([str(kw) for kw in post.keywords.all()]),
            }

            output_dir = args[0]
            filename = '{d.year:02}-{d.month:02}-{d.day:02}-{slug}.markdown'.format(
                    d=post.publish_date, slug=post.slug)

            content = post.content.encode('utf-8').replace('\r', '')

            # Write out the file
            with open(os.path.join(output_dir, filename), 'w') as fp:
                fp.write('---' + os.linesep)
                for k, v in header.items():
                    fp.write('%s: %s%s' % (k, v, os.linesep))
                fp.write('---' + os.linesep)
                fp.write(content)
