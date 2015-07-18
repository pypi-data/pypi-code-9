from __future__ import absolute_import

import os
import sys
import re


CF_SHARED_CDN = "d3jpl91pxevbkh.cloudfront.net"
OLD_AKAMAI_SHARED_CDN = "cloudinary-a.akamaihd.net"
AKAMAI_SHARED_CDN = "res.cloudinary.com"
SHARED_CDN = AKAMAI_SHARED_CDN
CL_BLANK = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"

VERSION = "1.1.3"
USER_AGENT = "CloudinaryPython/" + VERSION
""" :const: USER_AGENT """

USER_PLATFORM = ""
"""
Additional information to be passed with the USER_AGENT, e.g. "CloudinaryMagento/1.0.1". This value is set in platform-specific
implementations that use cloudinary_php.

The format of the value should be <ProductName>/Version[ (comment)].
@see http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.43

**Do not set this value in application code!**
"""

from cloudinary import utils
from cloudinary.compat import urlparse, parse_qs


def get_user_agent():
    """Provides the `USER_AGENT` string that is passed to the Cloudinary servers.
    Prepends  `USER_PLATFORM` if it is defined.

    :returns: the user agent
    :rtype: str
    """

    if USER_PLATFORM == "":
        return USER_AGENT
    else:
        return USER_PLATFORM + " " + USER_AGENT

def import_django_settings():
    try:
        import django.conf
        from django.core.exceptions import ImproperlyConfigured
        try:
            if 'CLOUDINARY' in dir(django.conf.settings):
                return django.conf.settings.CLOUDINARY
            else:
                return None
        except ImproperlyConfigured:
            return None
    except ImportError:
        return None

class Config(object):
    def __init__(self):
        django_settings = import_django_settings()
        if django_settings:
            self.update(**django_settings)
        elif os.environ.get("CLOUDINARY_CLOUD_NAME"):
            self.update(
              cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
              api_key = os.environ.get("CLOUDINARY_API_KEY"),
              api_secret = os.environ.get("CLOUDINARY_API_SECRET"),
              secure_distribution = os.environ.get("CLOUDINARY_SECURE_DISTRIBUTION"),
              private_cdn = os.environ.get("CLOUDINARY_PRIVATE_CDN") == 'true'
            )
        elif os.environ.get("CLOUDINARY_URL"):
            uri = urlparse(os.environ.get("CLOUDINARY_URL").replace("cloudinary://", "http://"))
            for k, v in parse_qs(uri.query).items():
                self.__dict__[k] = v[0]
            self.update(
              cloud_name = uri.hostname,
              api_key = uri.username,
              api_secret = uri.password,
              private_cdn = uri.path != ''
            )
            if uri.path != '':
                self.update(secure_distribution = uri.path[1:])
    def __getattr__(self, i):
        if i in self.__dict__:
            return self.__dict__[i]
        else:
            return None

    def update(self, **keywords):
        for k, v in keywords.items():
            self.__dict__[k] = v

_config = Config()

def config(**keywords):
    global _config
    _config.update(**keywords)
    return _config

def reset_config():
    global _config
    _config = Config()

class CloudinaryResource(object):
    def __init__(self, public_id = None, format = None, version = None,
            signature = None, url_options = {}, metadata = None, type = None, resource_type = None,
            default_resource_type=None):
        self.metadata = metadata
        metadata = metadata or {}
        self.public_id = public_id or metadata.get('public_id')
        self.format = format or metadata.get('format')
        self.version = version or metadata.get('version')
        self.signature = signature or metadata.get('signature')
        self.type = type or metadata.get('type') or "upload"
        self.resource_type = resource_type or metadata.get('resource_type')
        self.default_resource_type = default_resource_type
        self.url_options = url_options

    def __unicode__(self):
        return self.public_id

    def validate(self):
        expected = utils.api_sign_request({"public_id": self.public_id, "version": self.version}, config().api_secret)
        return self.signature == expected

    @property
    def url(self):
        return self.build_url(**self.url_options)

    def __build_url(self, **options):
        combined_options = dict(format = self.format, version = self.version, type = self.type, resource_type = self.resource_type or self.default_resource_type or "image")
        combined_options.update(options)
        public_id = combined_options.get('public_id') or  self.public_id
        return utils.cloudinary_url(public_id, **combined_options)
      
    def build_url(self, **options):
        return self.__build_url(**options)[0]

    def default_poster_options(self, options):
        options["format"] = options.get("format", "jpg")

    def default_source_types(self):
        return ['webm', 'mp4', 'ogv']

    def image(self, **options):
        if options.get("resource_type", self.resource_type or self.default_resource_type) == "video":
            self.default_poster_options(options)
        src, attrs = self.__build_url(**options)
        responsive = attrs.pop("responsive", False)
        hidpi = attrs.pop("hidpi", False)
        if responsive or hidpi:
            attrs["data-src"] = src
            classes = "cld-responsive" if responsive else "cld-hidpi"
            if "class" in attrs: classes += " " + attrs["class"] 
            attrs["class"] = classes
            src = attrs.pop("responsive_placeholder", config().responsive_placeholder)
            if src == "blank": src = CL_BLANK 
        
        if src: attrs["src"] = src

        return u"<img {0}/>".format(utils.html_attrs(attrs))

    def video_thumbnail(self, **options):
        self.default_poster_options(options)
        return self.build_url(**options)

    # Creates an HTML video tag for the provided +source+
    #
    # ==== Options
    # * <tt>source_types</tt> - Specify which source type the tag should include. defaults to webm, mp4 and ogv.
    # * <tt>source_transformation</tt> - specific transformations to use for a specific source type.
    # * <tt>poster</tt> - override default thumbnail:
    #   * url: provide an ad hoc url
    #   * options: with specific poster transformations and/or Cloudinary +:public_id+
    #
    # ==== Examples
    #   CloudinaryResource("mymovie.mp4").video()
    #   CloudinaryResource("mymovie.mp4").video(source_types = 'webm')
    #   CloudinaryResource("mymovie.ogv").video(poster = "myspecialplaceholder.jpg")
    #   CloudinaryResource("mymovie.webm").video(source_types = ['webm', 'mp4'], poster = {'effect': 'sepia'})
    def video(self, **options):
        public_id = options.get('public_id', self.public_id)
        source = re.sub("\.({0})$".format("|".join(self.default_source_types())), '', public_id)

        source_types          = options.pop('source_types', [])
        source_transformation = options.pop('source_transformation', {})
        fallback              = options.pop('fallback_content', '')
        options['resource_type'] = options.pop('resource_type', self.resource_type or self.default_resource_type or 'video')

        if len(source_types) == 0: source_types = self.default_source_types()
        video_options = options.copy()

        if 'poster' in video_options:
            poster_options = video_options['poster']
            if isinstance(poster_options, dict):
                if 'public_id' in poster_options:
                    video_options['poster'] = utils.cloudinary_url(poster_options['public_id'], **poster_options)[0]
                else:
                    video_options['poster'] = self.video_thumbnail(public_id=source, **poster_options)
        else:
            video_options['poster'] = self.video_thumbnail(public_id=source, **options)
        
        if not video_options['poster']: del video_options['poster']

        html = '<video ';

        nested_source_types = isinstance(source_types, list) and len(source_types) > 1 
        if not nested_source_types:
            source = source + '.' + utils.build_array(source_types)[0];

        video_url = utils.cloudinary_url(source, **video_options)
        video_options = video_url[1]
        if not nested_source_types:
            video_options['src'] = video_url[0]
        if 'html_width' in video_options: video_options['width'] = video_options.pop('html_width')
        if 'html_height' in video_options: video_options['height'] = video_options.pop('html_height')
        html = html + utils.html_attrs(video_options) + '>'

        if nested_source_types:
            for source_type in source_types:
                transformation = options.copy()
                transformation.update(source_transformation.get(source_type, {}))
                src = utils.cloudinary_url(source, format = source_type, **transformation)[0]
                video_type = "ogg" if source_type == 'ogv' else source_type
                mime_type = "video/" + video_type
                html = html + '<source ' + utils.html_attrs({'src': src, 'type': mime_type}) + '>'
        html = html + fallback
        html = html + '</video>'
        return html

class CloudinaryImage(CloudinaryResource):
    def __init__(self, public_id=None, **kwargs):
        super(CloudinaryImage, self).__init__(public_id=public_id, default_resource_type="image", **kwargs)

class CloudinaryVideo(CloudinaryResource):
    def __init__(self, public_id=None, **kwargs):
        super(CloudinaryVideo, self).__init__(public_id=public_id, default_resource_type="video", **kwargs)

