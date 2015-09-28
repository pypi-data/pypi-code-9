"""
Load and setup extensions
"""
import re
import warnings
import logging
import inspect
import functools
from six.moves.urllib.parse import urlparse
from flask import abort, request, current_app
from core import WebPortfolio
import utils
import humanize
import wp_markdown
import flask_cloudy
import flask_recaptcha
import flask_seasurf
import flask_kvsession
import flask_cache
import flask_login
import ses_mailer
import flask_mail
import flask_s3


__all__ = ["extends",
           "with_user_roles",
           "login_required",
           "no_login_required",
           "nav_menu",
           "mailer",
           "cache",
           "storage",
           "recaptcha",
           "csrf",
           "logger",
           "warn_missing_config"]

# ------------------------------------------------------------------------------
def extends(module, *args, **kwargs):
    """
    Decorator to extend a module to a view.
    The module can be a class or function. It will copy all the methods to the class

    ie:
        #Your module.py
        welcome_module(view, **kwargs):

            @route("/welcome-home")
            my_view():
                pass
            return my_view

        #Your view.py
        @extends(welcome_module)
        class Index(WebPortfolio):
            pass

    :param module: object
    :param args:
    :param kwargs:
    :return:
    """
    def wrap(view):
        return view.extends(module(view, *args, **kwargs))
    return wrap

# ------------------------------------------------------------------------------

# user_*

def user_authenticated():
    """
    A shortcut to check if a user is authenticated
    :return: bool
    """
    return True if flask_login.current_user and flask_login.current_user.is_authenticated else False

def user_not_authenticated():
    """
    A shortcut to check if user not authenticated.
    """
    return not user_authenticated()

def with_user_roles(*roles):
    """
    A decorator to check if user has any of the roles specified

    @with_user_roles('superadmin', 'admin')
    def fn():
        pass
    """
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if user_authenticated():
                if not flask_login.current_user.has_any_roles(*roles):
                    return abort(403)
            else:
                return abort(401)
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def with_user_permissions(*permissions):
    pass


def login_required(func):
    """
    A wrapper around the flask_login.login_required.
    But it also checks the presence of the decorator: @no_login_required
    On a "@login_required" class, method containing "@no_login_required" will
    still be able to access without authentication
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if "no_login_required" not in utils.get_decorators_list(func) \
                and user_not_authenticated():
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

def no_login_required(func):
    """
    Dummy decorator. @login_required will inspect the method
    to look for this decorator
    Use this decorator when you want do not require login in a "@login_required" class/method
    :param func:
    :return:
    """
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        return func(*args, **kwargs)
    return decorated_view

# ------------------------------------------------------------------------------
#
# @nav_menu
#
# Decorator to build navigation menu directly from the methods
# By default it will build the menu of the module, class an method
# If the class is also decorated, it will use the menu name as the top
# level name

_NAV_MENU_STACK = {}

def nav_menu(name, **kwargs):
    """
    Decorator to build navigation menu directly on the methods
    By default it will build the menu of the module, class an method
    If the class is also decorated, it will use the menu name as the top level name

    :param name: The menu name
    :param kwargs: extra options to pass into the menu or to move the menu somewhere else

        order int: The order of the menu in the set

        show (list of bool or callback): To hide and show menu. Accepts bool or
                    list of callback function the callback function must return
                    a bool to check if all everything is True to show or will be False
                    ** When this menu is inside of a menu set, or has parent, if you want
                    that page to be activated, but don't want to create a menu link,
                    for example: a blog read page, set show to False. It will know
                    the menu set is active

        endpoint string: By default the endpoint is built based on the method and class.
                    When set it will be used instead

        endpoint_kwargs dict: dict of k/v data for enpoint

        group: On class menu, it can be used to filter a menu set to display

        The args below will allow you to change where the menu is placed.
        By default they are set automatically

        __module: the module name. Usually if using another module
        __class: the class name class name in the module
        __method: The method name, to build endpoint. Changing this will cha
        __is_class: When the decorator is on the class instead of the method.
            This will be used to make the top level.
            Function not inside of class, may say it's a class, set __is_class = False

    :return:
    """
    def wrap(f):
        if name is not None:
            __module = kwargs.pop("__module", f.__module__)
            __class = kwargs.pop("__class", inspect.stack()[1][3])
            __is_class = kwargs.pop("__is_class", inspect.isclass(f))
            __method = kwargs.pop("__method", f.__name__)

            _push_nav_menu(__module=__module,
                           __class=__class,
                           __method=__method,
                           __is_class=__is_class,
                           name=name,
                           **kwargs)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return wrap

def _push_nav_menu(**kwargs):

    __module = kwargs.pop("__module")
    __class = kwargs.pop("__class")
    __method = kwargs.pop("__method")
    __is_class = kwargs.pop("__is_class")

    __cls = __method if __is_class else __class
    path = "%s.%s" % (__module, __cls)

    if path not in _NAV_MENU_STACK:
        _NAV_MENU_STACK[path] = {
            "name": None,
            "endpoint": None,
            "endpoint_kwargs": {},
            "order": None,
            "sub_menu": [],
            "kwargs": {}
        }

    if "name" not in kwargs:
        raise TypeError("Missing 'name' in menu decorator")

    kwargs["endpoint"] = kwargs.pop("endpoint", "%s:%s" % (__cls,
                                                         "index" if __is_class else __method ))
    kwargs["endpoint_kwargs"] = kwargs.pop("endpoint_kwargs", {})
    order = kwargs.pop("order", 0)
    name = kwargs.pop("name")
    endpoint = kwargs.pop("endpoint")

    # show: accepts a bool or list of callback to execute
    show = kwargs.pop("show", [])

    if isinstance(show, bool):
        show = [show]
    elif show and not isinstance(show, list):
        show = [show]

    kwargs["show"] = show
    kwargs["__active"] = None
    kwargs["__index"] = None

    if __is_class:  # class menu
        kwargs["endpoint"] = endpoint
        kwargs["group"] = kwargs.pop("group", None)
        _NAV_MENU_STACK[path]["name"] = name
        _NAV_MENU_STACK[path]["order"] = order
        _NAV_MENU_STACK[path]["kwargs"] = kwargs
    else:  # sub menu
        menu = (order, name, endpoint, kwargs)
        _NAV_MENU_STACK[path]["sub_menu"].append(menu)

def _nav_menu_test_show(shows):
    return all([x() if hasattr(x, "__call__") else x for x in shows])

def _nav_menu_init(app):
    @app.before_request
    def p(*args, **kwargs):

        # (order, Name, sub_menu, **kargs, hidden_submenu)
        menu_list = []
        menu_index = 0
        for _, menu in _NAV_MENU_STACK.items():
            menu_index += 1

            menu["kwargs"]["__index"] = menu_index
            menu["kwargs"]["__active"] = False

            # Filter out menu that should not be shown
            _kw = menu["kwargs"]
            if _kw and "show" in _kw and _nav_menu_test_show(_kw["show"]) is False:
                continue

            sub_menu = []
            sub_menu_hidden = []  # Save all the hidden submenu

            for s in menu["sub_menu"]:
                if s[2] == request.endpoint:
                    s[3]["__active"] = True
                    menu["kwargs"]["__active"] = True

                sub_menu_hidden.append(s)

                _kw = s[3]
                if _kw and "show" in _kw and _nav_menu_test_show(_kw["show"]) is False:
                    continue
                sub_menu.append(s)

            _kwargs = menu["kwargs"]
            _kwargs["__hidden"] = sorted(sub_menu_hidden)
            menu_list.append((
                menu["order"],
                menu["name"],
                sorted(sub_menu),
                _kwargs
            ))

        WebPortfolio.g(NAV_MENU=sorted(menu_list))

WebPortfolio.bind(_nav_menu_init)

# ------------------------------------------------------------------------------

# Session
#
# It uses KV session to allow multiple backend for the session
def _session(app):
    store = None
    uri = app.config.get("SESSION_URI")
    if uri:
        parse_uri = urlparse(uri)
        scheme = parse_uri.scheme
        username = parse_uri.username
        password = parse_uri.password
        hostname = parse_uri.hostname
        port = parse_uri.port
        bucket = parse_uri.path.strip("/")

        if "redis" in scheme:
            import redis
            from simplekv.memory.redisstore import RedisStore
            conn = redis.StrictRedis.from_url(url=uri)
            store = RedisStore(conn)
        elif "s3" in scheme or "google_storage" in scheme:
            from simplekv.net.botostore import BotoStore
            import boto
            if "s3" in scheme:
                _con_fn = boto.connect_s3
            else:
                _con_fn = boto.connect_gs
            conn = _con_fn(username, password)
            _bucket = conn.create_bucket(bucket)
            store = BotoStore(_bucket)
        elif "memcache" in scheme:
            import memcache
            from simplekv.memory.memcachestore import MemcacheStore
            host_port = "%s:%s" % (hostname, port)
            conn = memcache.Client(servers=[host_port])
            store = MemcacheStore(conn)
        elif "sql" in scheme:
            from simplekv.db.sql import SQLAlchemyStore
            from sqlalchemy import create_engine, MetaData
            engine = create_engine(uri)
            metadata = MetaData(bind=engine)
            store = SQLAlchemyStore(engine, metadata, 'kvstore')
            metadata.create_all()
        else:
            raise ValueError("Invalid Session Store")
    if store:
        flask_kvsession.KVSessionExtension(store, app)

WebPortfolio.bind(_session)

# ------------------------------------------------------------------------------
# Mailer
class _Mailer(object):
    """
    A simple wrapper to switch between SES-Mailer and Flask-Mail based on config
    """
    mail = None
    provider = None
    config = None
    _template = None

    def init_app(self, app):
        self.config = app.config
        scheme = None

        mailer_uri = self.config.get("MAILER_URI")
        if mailer_uri:
            mailer_uri = urlparse(mailer_uri)
            scheme = mailer_uri.scheme

            # Using ses-mailer
            if "ses" in scheme:
                self.provider = "SES"

                access_key = mailer_uri.username or app.config.get("AWS_ACCESS_KEY_ID")
                secret_key = mailer_uri.password or app.config.get("AWS_SECRET_ACCESS_KEY")

                self.mail = ses_mailer.Mail(aws_access_key_id=access_key,
                                            aws_secret_access_key=secret_key,
                                            sender=self.config.get("MAILER_SENDER"),
                                            reply_to=self.config.get("MAILER_REPLY_TO"),
                                            template=self.config.get("MAILER_TEMPLATE"),
                                            template_context=self.config.get("MAILER_TEMPLATE_CONTEXT"))

            # SMTP will use flask-mail
            elif "smtp" in scheme:
                self.provider = "SMTP"

                class _App(object):
                    config = {
                        "MAIL_SERVER": mailer_uri.hostname,
                        "MAIL_USERNAME": mailer_uri.username,
                        "MAIL_PASSWORD": mailer_uri.password,
                        "MAIL_PORT": mailer_uri.port,
                        "MAIL_USE_TLS": True if "tls" in mailer_uri.scheme else False,
                        "MAIL_USE_SSL": True if "ssl" in mailer_uri.scheme else False,
                        "MAIL_DEFAULT_SENDER": app.config.get("MAILER_SENDER"),
                        "TESTING": app.config.get("TESTING"),
                        "DEBUG": app.config.get("DEBUG")
                    }
                    debug = app.config.get("DEBUG")
                    testing = app.config.get("TESTING")

                _app = _App()
                self.mail = flask_mail.Mail(app=_app)

                _ses_mailer = ses_mailer.Mail(template=self.config.get("MAILER_TEMPLATE"),
                                              template_context=self.config.get("MAILER_TEMPLATE_CONTEXT"))
                self._template = _ses_mailer.parse_template
            else:
                warnings.warn("Mailer Error. Invalid scheme '%s'>" % scheme)

    def send(self, to, subject, body, reply_to=None, **kwargs):
        """
        Send simple message
        """
        if self.provider == "SES":
            self.mail.send(to=to,
                           subject=subject,
                           body=body,
                           reply_to=reply_to,
                           **kwargs)

        elif self.provider == "SMTP":
            msg = flask_mail.Message(recipients=[to] if not isinstance(to, list) else to,
                                     subject=subject,
                                     body=body,
                                     reply_to=reply_to,
                                     sender=self.config.get("MAILER_SENDER"))
            self.mail.send(msg)
        else:
            abort(500, "Mailer Error. Invalid 'provider'")

    def send_template(self, template, to, reply_to=None, **context):
        """
        Send Template message
        """
        if self.provider == "SES":
            self.mail.send_template(template=template,
                                    to=to,
                                    reply_to=reply_to,
                                    **context)

        elif self.provider == "SMTP":
            data = self._template(template=template, **context)
            msg = flask_mail.Message(recipients=[to] if not isinstance(to, list) else to,
                                     subject=data["subject"],
                                     body=data["body"],
                                     reply_to=reply_to,
                                     sender=self.config.get("MAILER_SENDER"))
            self.mail.send(msg)
        else:
            abort(500, "Mailer Error. Invalid 'provider'")

mailer = _Mailer()
WebPortfolio.bind(mailer.init_app)

# ------------------------------------------------------------------------------

# Assets Delivery
class _AssetsDelivery(flask_s3.FlaskS3):

    def init_app(self, app):
        delivery_method = app.config.get("ASSETS_DELIVERY_METHOD")
        if delivery_method and delivery_method.upper() in ["S3", "CDN"]:
            #with app.app_context():
            is_secure = False #request.is_secure

            if delivery_method.upper() == "CDN":
                domain = app.config.get("ASSETS_DELIVERY_DOMAIN")
                if "://" in domain:
                    domain_parsed = urlparse(domain)
                    is_secure = domain_parsed.scheme == "https"
                    domain = domain_parsed.netloc
                app.config.setdefault("S3_CDN_DOMAIN", domain)

            app.config["FLASK_ASSETS_USE_S3"] = True
            app.config["USE_S3"] = True
            app.config.setdefault("S3_USE_HTTPS", is_secure)
            app.config["S3_URL_STYLE"] = "path"
            app.config.setdefault("S3_ONLY_MODIFIED", False)
            app.config.setdefault("S3_BUCKET_NAME", app.config.get("AWS_S3_BUCKET_NAME"))

            super(self.__class__, self).init_app(app)

assets_delivery = _AssetsDelivery()
WebPortfolio.bind(assets_delivery.init_app)

# ------------------------------------------------------------------------------

# Cache
cache = flask_cache.Cache()
WebPortfolio.bind(cache.init_app)

# Storage
storage = flask_cloudy.Storage()
WebPortfolio.bind(storage.init_app)

# Recaptcha
recaptcha = flask_recaptcha.ReCaptcha()
WebPortfolio.bind(recaptcha.init_app)

# CSRF
csrf = flask_seasurf.SeaSurf()
WebPortfolio.bind(csrf.init_app)

# LOGGER
logger = logging

def warn_missing_config(conf, k):
    if k not in conf or not conf.get(k) or conf.get(k).strip() == "":
        msg = "Config [ %s ] value is not set or empty" % k
        logger.warn(msg)
        return msg
    return None

# ------------------------------------------------------------------------------

def _setup(app):

    def sanity_check():
        keys = [
            "APPLICATION_ADMIN_EMAIL",
            "MAILER_URI",
            "MAILER_SENDER",
            "MODULE_CONTACT_PAGE_EMAIL",
            "RECAPTCHA_SITE_KEY",
            "RECAPTCHA_SECRET_KEY"
        ]
        [warn_missing_config(app.config, k) for k in keys]

    sanity_check()

    WebPortfolio.g(APPLICATION_NAME=app.config.get("APPLICATION_NAME"),
                   APPLICATION_VERSION=app.config.get("APPLICATION_VERSION"),
                   APPLICATION_URL=app.config.get("APPLICATION_URL"),
                   APPLICATION_GOOGLE_ANALYTICS_ID=app.config.get("APPLICATION_GOOGLE_ANALYTICS_ID"))

    # Setup filters
    @app.template_filter('datetime')
    def format_datetime(dt, format="%m/%d/%Y"):
        return "" if not dt else dt.strftime(format)

    @app.template_filter('strip_decimal')
    def strip_decimal(amount):
        return amount.split(".")[0]

    @app.template_filter('bool_to_yes')
    def bool_to_yes(b):
        return "Yes" if b else "No"

    @app.template_filter('bool_to_int')
    def bool_to_int(b):
        return 1 if b else 0

    @app.template_filter('nl2br')
    def nl2br(s):
        """
        {{ s|nl2br }}

        Convert newlines into <p> and <br />s.
        """
        if not isinstance(s, basestring):
            s = str(s)
        s = re.sub(r'\r\n|\r|\n', '\n', s)
        paragraphs = re.split('\n{2,}', s)
        paragraphs = ['<p>%s</p>' % p.strip().replace('\n', '<br />') for p in paragraphs]
        return '\n\n'.join(paragraphs)

    # More filters
    app.jinja_env.filters.update({
        # slug
        "slug": utils.slugify,
        # Transform an int to comma
        "int_with_comma": humanize.intcomma,
        # Show the date ago: Today, yesterday, July 27 (without year in same year), July 15 2014
        "date_since": humanize.naturaldate,
        # To show the time ago: 3 min ago, 2 days ago, 1 year 7 days ago
        "time_since": humanize.naturaltime,
        # Return a mardown to HTML
        "markdown": wp_markdown.html,
        # Create a Table of Content of the Markdown
        "markdown_toc": wp_markdown.toc
    })

WebPortfolio.bind(_setup)


