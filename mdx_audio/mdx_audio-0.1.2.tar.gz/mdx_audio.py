# coding: utf-8

"""
Audio tags

>>> import markdown

Test One Audio tag

>>> s = "::audio[my title](/url/1.mp3)"
>>> markdown.markdown(s, ['audio'])
'<p><audio controls="controls"><source src="/url/1.mp3" type="audio/mp3"></source></audio></p>'

Test Two Audio tags

>>> s = "::audio[my title](/url/1.mp3 /url/2.ogg)"
>>> markdown.markdown(s, ['audio'])
'<p><audio controls="controls"><source src="/url/1.mp3" type="audio/mp3"></source><source src="/url/2.ogg" type="audio/ogg"></source></audio></p>'

Test Two Audio tags remove commas

>>> s = "::audio[my title](/url/1.mp3, /url/2.ogg)"
>>> markdown.markdown(s, ['audio'])
'<p><audio controls="controls"><source src="/url/1.mp3" type="audio/mp3"></source><source src="/url/2.ogg" type="audio/ogg"></source></audio></p>'
"""

from __future__ import print_function, unicode_literals, absolute_import
import markdown
from markdown.inlinepatterns import Pattern
from markdown.util import etree


__version__ = '0.1.2'


__author__ = 'Panos Kountanis'


class AudioExtension(markdown.Extension):
    configs = {}
    def __init__(self, configs):
        for k, v in configs or {}:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        pattern = r'(?:(?:^::+))(?P<format>[\w+-]*)\[(?P<title>[\w\s\d+]*)\]\((?P<urls>[\w\d\W+]*)\)'
        inline_audio_pattern = AudioPattern(pattern)
        inline_audio_pattern.ext = self
        md.inlinePatterns.add('audio', inline_audio_pattern, '<reference')


class AudioPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        audio = etree.Element('audio')
        audio.set('controls', 'controls')

        audio_format = m.group('format')
        audio_title = m.group('title')
        audio_urls = m.group('urls')

        for url in audio_urls.replace(',', '').split(' '):
            ext = url.split('.')[-1]
            src = etree.Element('source')
            src.set('src', url.strip())
            src.set('type', 'audio/{0}'.format(ext))
            audio.append(src)
        return audio


def makeExtension(configs=None):
    return AudioExtension(configs=configs)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
