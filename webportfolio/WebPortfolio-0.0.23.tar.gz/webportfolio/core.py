"""
WebPortfolio

"""
import os
import datetime
import inspect
import utils
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.routing import BaseConverter
from flask import Flask, render_template, flash, session, url_for
from flask_classy import FlaskView, route
from flask_assets import Environment
import jinja2
import warnings
import __about__

# ------------------------------------------------------------------------------


NAME = __about__.name
__version__ = __about__.version
__author__ = __about__.author
__license__ = __about__.license
__copyright__ = __about__.copyright

# ------------------------------------------------------------------------------

__all__ = ["WebPortfolio",
           "get_env",
           "get_env_config",
           "flash_error",
           "flash_success",
           "flash_info",
           "flash_data",
           "get_flashed_data",
           "route"]

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

class WebPortfolio(FlaskView):
    """ WebPortfolio """
    LAYOUT = "layout.html"  # The default layout
    PAGE_META = "PAGE_META"
    GLOBAL_KEY_CONTEXT = "__g"
    assets = None
    _app = None
    _bind = set()
    _template_paths = set()
    _static_paths = set()
    _asset_bundles = set()
    _default_page_meta = dict(
            title="",
            description="",
            url="",
            image="",
            site_name="",
            object_type="article",
            locale="",
            keywords=[],
            use_opengraph=True,
            use_googleplus=True,
            use_twitter=True,
            properties={}
        )
    _global = dict(
        WEBPORTFOLIO_NAME=NAME,
        WEBPORTFOLIO_VERSION=__version__,
        YEAR=datetime.datetime.now().year,
        PAGE_META=_default_page_meta
    )

    @classmethod
    def init(cls, flask_or_import_name, project=None, directory=None, config=None,
             compress_html=True):
        """
        Allow to register all subclasses of WebPortfolio at once

        If a class doesn't have a route base, it will create a dasherize version
        of the class name.

        So we call it once initiating
        :param flask_or_import_name: Flask instance or import name -> __name__
        :param project: name of the project. If the directory and config is empty, it will guess them from here
        :param directory: The directory containing your project's Views, Templates and Static
        :param config: string of config object. ie: "app.config.Dev"
        :param compress_html: bool - If true it will use the plugin "jinja2htmlcompress"
                to remove white spaces off the html resul
        """

        if isinstance(flask_or_import_name, Flask):
            app = flask_or_import_name
        else:
            app = Flask(flask_or_import_name)

        app.wsgi_app = ProxyFix(app.wsgi_app)

        app.url_map.converters['regex'] = RegexConverter

        if not directory:
            directory = "application/%s" % project if project else "."

        if not config:
            config = "application.config.%s" % get_env()

        app.config.from_object(config)

        if directory:
            app.template_folder = directory + "/templates"
            app.static_folder = directory + "/static"

        cls.add_asset_bundle(app.static_folder)

        # Extensions to remove extra white spaces in html
        if compress_html:
            app.jinja_env.add_extension('webportfolio.jinja2htmlcompress.HTMLCompress')

        cls._app = app

        # Flask Assets
        cls.assets = Environment(cls._app)

        # Register templates
        if cls._template_paths:
            loader = [cls._app.jinja_loader] + list(cls._template_paths)
            cls._app.jinja_loader = jinja2.ChoiceLoader(loader)

        # Register static
        if cls._static_paths:
            loader = [cls._app.static_folder] + list(cls._static_paths)
            cls.assets.load_path = loader

        # init_app
        for _app in cls._bind:
            _app(cls._app)

        # Register all views
        for subcls in cls.__subclasses__():
            route_base = subcls.route_base
            if not route_base:
                route_base = utils.dasherize(utils.underscore(subcls.__name__))
            subcls.register(cls._app, route_base=route_base)

        # Load all bundles
        for a in cls._asset_bundles:
            cls.assets.from_yaml(a)

        @cls._app.after_request
        def _before_request_cleanup(response):
            cls._global["PAGE_META"] = cls._default_page_meta
            cls._global["PAGE_META"]["site_name"] = cls._app.config.get("APPLICATION_NAME", "")
            return response

        return cls._app

    @classmethod
    def bind(cls, kls):
        """
        To bind middlewares that needs the 'app' object to init
        Bound middlewares will be assigned on cls.init()
        """
        if not hasattr(kls, "__call__"):
            raise TypeError("From WebPortfolio.bind: '%s' is not callable" % kls)
        cls._bind.add(kls)
        return kls

    @classmethod
    def render(cls, data={}, view_template=None, layout=None, **kwargs):
        """
        To render data to the associate template file of the action view
        :param data: The context data to pass to the template
        :param view_template: The file template to use. By default it will map the classname/action.html
        :param layout: The body layout, must contain {% include __template__ %}
        """
        if not view_template:
            stack = inspect.stack()[1]
            module = inspect.getmodule(cls).__name__
            module_name = module.split(".")[-1]
            action_name = stack[3]      # The method being called in the class
            view_name = cls.__name__    # The name of the class without View

            if view_name.endswith("View"):
                view_name = view_name[:-4]
            view_template = "%s/%s.html" % (view_name, action_name)

        data = data or dict()
        data["__g"] = cls._global
        if kwargs:
            data.update(kwargs)

        data["__template__"] = view_template

        return render_template(layout or cls.LAYOUT, **data)

    @classmethod
    def g(cls, **kwargs):
        """
        Assign a global view context to be used in the template
        :params **kwargs:
        """
        cls._global.update(kwargs)
        
    @classmethod
    def config(cls, key, default=None):
        """
        Shortcut to access the config in your class
        :param key: The key to access
        :param default: The default value when None
        :returns mixed:
        """
        return cls._app.config.get(key, default)

    @classmethod
    def page_meta(cls, **kwargs):
        """
        Meta allows you to add meta data to site
        :params **kwargs:

        meta keys we're expecting:
            title (str)
            description (str)
            url (str) (Will pick it up by itself if not set)
            image (str)
            site_name (str) (but can pick it up from config file)
            object_type (str)
            keywords (list)
            locale (str)
            card (str)

            **Boolean By default these keys are True
            use_opengraph
            use_twitter
            use_googleplus

        """
        n = cls.PAGE_META
        page_meta = cls._global.get(n, {})
        page_meta.update(**kwargs)
        cls.g(n=page_meta)

    @classmethod
    def register_module(cls, root_pkg=None, template="templates", static="static"):
        """
        Register a module's template directory and static
        :param root_pkg: str - The root dir,
                        or the dotted resource package (package.path.path,
                        usually __name__ of templates and static
        :param template: str - The template dir name. If root_dir is none,
                        template should be a path
        :param static: str - The static dir name. If root_dir is none,
                        static should be a path
        """
        if root_pkg:
            if not os.path.isdir(root_pkg) and "." in root_pkg:
                root_pkg = utils.get_pkg_resources_filename(root_pkg)

            template_path = os.path.join(root_pkg, template)
            static_path = os.path.join(root_pkg, static)
        else:
            template_path = template
            static_path = static

        if os.path.isdir(template_path):
            template_path = jinja2.FileSystemLoader(template_path)
            cls._template_paths.add(template_path)
        else:
            warnings.warn("Module registration: Not a <template> directory '%s' " % template_path)

        if os.path.isdir(static_path):
            cls._static_paths.add(static_path)
            cls.add_asset_bundle(static_path)
        else:
            warnings.warn("Module registration: Not a <static> directory '%s' " % static_path)

    @classmethod
    def add_asset_bundle(cls, path):
        """
        Add a webassets bundle yml file
        """
        f = "%s/assets.yml" % path
        if os.path.isfile(f):
            cls._asset_bundles.add(f)

    @classmethod
    def extends(cls, kls):
        """
        A view decorator to extend another view class or function to itself
        It will inherit all its methods and propeties and use them on itself

        -- EXAMPLES --

        class Index(WebPortfolio):
            pass

        index = Index()

        ::-> As decorator on classes ::
        @index.extends__
        class A(object):
            def hello(self):
                pass

        @index.extends__
        class C()
            def world(self):
                pass

        ::-> Decorator With function call ::
        @index.extends__
        def hello(self):
            pass

        """
        if inspect.isclass(kls):
            for _name, _val in kls.__dict__.items():
                if not _name.startswith("__"):
                    setattr(cls, _name, _val)
        elif inspect.isfunction(kls):
            setattr(cls, kls.__name__, kls)
        return cls

def get_env():
    """
    Return the Capitalize environment name
    It can be used to retrieve class base config
    Default: Development
    :returns: str
    """
    env_key = "WEBPORTFOLIO_ENV"
    env = "Development"
    if env_key in os.environ:
        env = os.environ[env_key].lower().capitalize()
    return env

def get_env_config(config):
    """
    Return config class
    :param config : Object - The configuration module containing the environment object
    """
    return getattr(config, get_env())

# Flashing
def flash_error(message):
    """ Set an error message """
    flash(message, "error")

def flash_success(message):
    """ Set an success message """
    flash(message, "success")

def flash_info(message):
    """ Set an info message """
    flash(message, "info")

def flash_data(data):
    """
    Just like flash, but will save data
    :param data:
    :return:
    """
    session["_flash_data"] = data

def get_flashed_data():
    """
    Retrieved
    :return: mixed
    """
    return session.pop("_flash_data", None)
