# -*- coding: utf-8 -*-
"""The `pyneric.rest_requests` module contains REST resource classes."""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from pyneric.future import *
from future.standard_library import install_aliases
install_aliases()

import inspect
import functools
from urllib.parse import quote, unquote, urljoin, urlsplit, urlunsplit

from pyneric.meta import Metaclass
from pyneric import util
from pyneric.util import tryf


__all__ = []

_ENCODING = 'UTF-8'
"""Assumed string encoding (matches quote/unquote default)"""

SEPARATOR = '/'
"""URL path separator"""


def _ensure_text(value, coerce=True):
    return ensure_text(value, _ENCODING, coerce=coerce)


def _unquote(string):
    return unquote(string, errors='strict')


def _url_join(base, path, safe=''):
    base = _ensure_text(base)
    path = quote(_ensure_text(path), safe=safe)
    if base.endswith(SEPARATOR):
        if not path.endswith(SEPARATOR):
            path += SEPARATOR
    else:
        base += SEPARATOR
    return urljoin(base, path)


def _url_split(url):
    result = list(urlsplit(url))
    result[2] = result[2].rstrip(SEPARATOR)
    result[3:] = '', ''
    return result


class _RestMetaclass(Metaclass):

    __metadata__ = dict(url_path=None, container_class=None,
                        container_is_collection=False,
                        reference_attribute=None)
    __propagate__ = tuple(__metadata__) + ('is_abstract',)

    @staticmethod
    def validate_url_path(value):
        if value is None:
            return  # Resource is abstract; no further validation is necessary.
        try:
            _ensure_text(value, coerce=False)
        except TypeError:
            raise TypeError(
                "invalid url_path attribute (not string): {!r}"
                .format(value))
        except UnicodeDecodeError:
            raise ValueError(
                "invalid url_path attribute (not valid {}): {!r}"
                .format(_ENCODING, value))
        if not value:
            raise ValueError(
                "invalid url_path attribute (empty): {!r}"
                .format(value))
        elif value.startswith(SEPARATOR):
            raise ValueError(
                "invalid url_path attribute (leading slash): {!r}"
                .format(value))

    @staticmethod
    def validate_container_class(value):
        if not (value is None or
                inspect.isclass(value) and
                issubclass(value, RestResource)):
            raise TypeError(
                "invalid container_class attribute: {!r}"
                .format(value))

    @staticmethod
    def validate_reference_attribute(value):
        if value is None:
            return
        try:
            util.valid_python_identifier(value, exception=True)
        except (TypeError, UnicodeDecodeError, ValueError) as exc:
            raise type(exc)(
                "invalid reference_attribute attribute: {!r} ({})"
                .format(value, exc))

    @property
    def is_abstract(cls):
        """Return whether this resource class is abstract (no url_path)."""
        return cls.url_path is None


@util.add_to_all
class RestResource(future.with_metaclass(_RestMetaclass, object)):

    """A standard REST resource.

    A REST resource is represented by a (usually HTTP) URL, which is specified
    in this class via the combination of the `container` passed to the
    constructor and the :attr:`url_path`.  See the attribute documentation for
    more details.

    """

    url_path = None
    """Path segment(s) identifying the REST resource.

    This may be `None` to signify that this is an abstract resource; otherwise,
    it is the path under the base (API root or containing resource) identifying
    this resource, which will be automatically URL-quoted (except for path
    separators) when it is included in a URL produced by the library.

    This may contain path separator(s) ("/") if there is no need to access the
    path segments as distinct REST resources.

    This cannot start with a path separator, but it may end with one if this
    and resources under this one (i.e., those that use this one as container)
    shall each have a trailing path separator.  If the `container` passed to
    the constructor is a URL string with a trailing slash or a
    :class:`RestResource` with a `url_path` ending with a path separator, then
    it is not significant whether this value has a trailing path separator,
    since all resources under that container are represented with a trailing
    path separator.

    """

    container_class = None
    """The parent REST resource that contains this resource.

    The `container` passed to the constructor must be an instance of this
    resource.  If this is `None`, then the `container` passed to the
    constructor must be a URL string under which this resource resides.

    An attribute named after this class or explicitly named by this class is
    created to reference the instance passed to the constructor as `container`.

    """

    container_is_collection = False
    """Whether the containing resource is the specified collection.

    This only applies when the :attr:`container_class` is a subclass of
    `RestCollection`; it is simply a convenience for automatically confirming
    the resource's validity within the REST API.

    If this is false, then this resource exists under each member of the
    collection; otherwise, it exists directly under the collection itself.

    """

    reference_attribute = None
    """The attribute name used to refer to this resource.

    For example, this applies when another resource refers to this one as the
    container.

    If this is `None` (the default), then the attribute used to refer to this
    resource (as container) is the class name converted to lower-case and
    underscored (with additional underscore(s) appended when it would conflict
    with existing attributes in the referring resource).

    """

    def __init__(self, container):
        def invalid_for_type(reason=None):
            message = ("Container {!r} is invalid for resource type {!r}."
                       .format(container, type(self)))
            if reason:
                message += "  " + reason
            raise ValueError(message)
        if self.is_abstract:
            raise TypeError(
                "{!r} is an abstract RestResource and cannot be instantiated."
                .format(type(self)))
        self._container = container
        if self.container_class:
            if not (isinstance(container, self.container_class) and
                    (not issubclass(self.container_class, RestCollection) or
                     self.container_is_collection is None or
                     bool(self.container_is_collection) is
                     (container.id is None))):
                invalid_for_type()
            attr = self.container_class.reference_attribute
            if not attr:
                attr = util.underscore(self.container_class.__name__)
                while hasattr(self, attr):
                    attr += '_'
            setattr(self, attr, container)
            container = container.url
        elif not isinstance(container, basestring):
            invalid_for_type("It must be a string (URL).")
        self._url = _url_join(container, self.url_path, safe=SEPARATOR)

    @classmethod
    def from_url(cls, url):
        """Construct an instance of this resource based on the given URL."""
        try:
            return cls._from_url(url)
        except Exception as exc:
            raise ValueError(
                "The URL {!r} is invalid for {}.  {}"
                .format(url, cls.__name__, exc))

    @classmethod
    def _from_url(cls, url, **kwargs):
        container = cls._get_container_from_url(url)
        if cls.container_class:
            container = cls.container_class.from_url(container)
        return cls(container, **kwargs)

    @classmethod
    def _get_container_from_url(cls, url):
        original_url, url = url, _ensure_text(url)
        url_split = _url_split(url)
        segments = [quote(_unquote(x)) for x in url_split[2].split(SEPARATOR)]
        resource_segments = (quote(_ensure_text(cls.url_path))
                             .rstrip(SEPARATOR).split(SEPARATOR))
        size = len(resource_segments)
        if segments[-size:] != resource_segments:
            multiple = size != 1
            raise ValueError(
                "The last {}segment{} of the URL {!r} {} invalid for {}."
                .format("{} ".format(size) if multiple else "",
                        "s" if multiple else "", original_url,
                        "are" if multiple else "is", cls.__name__))
        url_split[2] = SEPARATOR.join(segments[:-size])
        return urlunsplit(url_split)

    def __getattr__(self, item):
        try:
            import requests
        except ImportError:  # pragma: no cover
            pass
        else:
            try:
                func = getattr(requests, item)
            except AttributeError:
                pass
            else:
                if (inspect.isfunction(func) and
                    'url' in (inspect.getargspec(func).args if future.PY2 else
                              inspect.signature(func).parameters)):
                    return functools.partial(func, url=self.url)
        util.raise_attribute_error(self, item)

    @property
    def container(self):
        """The container of this resource.

        This is an instance of :attr:`container_class` if that is not `None`;
        otherwise, this is the URL under which this resource resides.

        Whether the container has a trailing slash determines whether the
        resource's URL includes a trailing slash.

        """
        return self._container

    @property
    def url(self):
        """The complete URL of the resource."""
        return self._url


class _RestCollectionMetaclass(_RestMetaclass):

    __metadata__ = dict(id_type=str)
    __propagate__ = tuple(__metadata__)

    @classmethod
    def validate_id_type(cls, value):
        if not inspect.isclass(value):
            raise TypeError(
                "invalid id_type attribute: {!r}"
                .format(value))


@util.add_to_all
class RestCollection(future.with_metaclass(_RestCollectionMetaclass,
                                           RestResource)):

    """A standard REST collection.

    This is a special type of resource in REST where a set of usually
    homogeneous, but at least related, resources are contained within a
    collection.  The collection is represented by the `url_path` (usually a
    plural noun) and each member of the collection is represented by a unique
    identifier under the collection in the URL path.  For example, a collection
    called "resources" might have individual members of the collection
    represented by "resources/1" and "resources/2".  In this case, "resources"
    would be the :attr:`url_path`, and "1" and "2" would be the values for
    :attr:`id`.

    An instance will represent either the collection or a member of the
    collection, depending on the `id` argument passed to the constructor.

    """

    id_type = str
    """The type of the :attr:`id` attribute.

    The :attr:`id_type` is `str` by default, since that is how it is
    represented in the resource URL, but it can be set to another type if the
    :attr:`id` attribute should be accepted and presented differently from its
    string representation.

    """

    def __init__(self, container, id=None):
        """Initialize an instance of this REST collection or a member.

        :param str/RestResource container: See :attr:`RestResource.container`.
        :param id: See :attr:`id`.

        The instance represents the collection when `id` is `None`; otherwise,
        it represents one of its members.

        """
        super().__init__(container)
        self._id = id = self.validate_id(id)
        if id is None:
            return
        self._url = _url_join(self._url, id)

    @classmethod
    def _from_url(cls, url, **kwargs):
        assert not kwargs, ("RestCollection._from_url should never receive "
                            "keyword arguments.")
        super_method = super()._from_url
        try:
            result = super_method(url)
        except ValueError:
            result = None
        url_split = _url_split(_ensure_text(url))
        url_split[2], id = url_split[2].rsplit(SEPARATOR, 1)
        try:
            id = cls.validate_id(_unquote(id))
        except ValueError:
            if result:
                return result
            raise
        collection_url = urlunsplit(url_split)
        try:
            member_result = super_method(collection_url, id=id)
        except ValueError:
            if result:
                return result
            raise
        if result:
            raise ValueError(
                "The URL {!r} is ambiguous for {} as to whether "
                "it is for the collection or one of its members."
                .format(url, cls.__name__))
        return member_result

    @classmethod
    def validate_id(cls, value):
        """Validate the given value as a valid identifier for this resource."""
        if value is None:
            return
        id = value
        if not isinstance(value, cls.id_type):
            try:
                id = cls.id_type(id)
            except Exception as exc:
                raise ValueError(
                    "The id {!r} cannot be cast to {!r}.  {}"
                    .format(value, cls.id_type, str(exc)))
        if not tryf(str, id):
            raise ValueError(
                "The id {!r} has no string representation."
                .format(value))
        return id

    @property
    def id(self):
        """The identifier of the member within the REST collection.

        This is `None` if this instance represents the entire collection.

        The value provided to the constructor must be one of:

        * `None`
        * an instance of :attr:`id_type`
        * a value that can be passed alone to :attr:`id_type`

        In the last case, the object that results from the instantiation
        becomes the value of this property.

        Like :attr:`url_path`, when this value is included in a URL produced
        by the library, it is automatically cast to a string and URL-quoted,
        except that path separators (slashes) in :attr:`id` are also quoted.

        """
        return self._id
