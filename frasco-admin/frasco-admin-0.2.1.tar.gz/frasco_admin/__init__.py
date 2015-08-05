from frasco import Feature, action, Blueprint, current_app, hook, signal
from frasco.utils import import_string
from .view import AdminView, AdminBlueprint
from blueprint import admin_bp
import os


class AdminFeature(Feature):
    name = "admin"
    requires = ["bootstrap"]
    blueprints = [admin_bp]
    view_files = [("admin/*", AdminView)]
    defaults = {"url_prefix": "/admin",
                "subdomain": None}

    init_admin_signal = signal('init_admin')

    def init_app(self, app):
        self.app = app
        self.admin_checker_func = None
        app.features.menu.ensure("admin")
        
        app.assets.register({
            "admin": [
                "@jquery-bootstrap-all-cdn",
                "@font-awesome-cdn",
                "admin/layout.css",
                "admin/admin.js"]})

        app.jinja_env.macros.register_file(
            os.path.join(os.path.dirname(__file__), "macros.html"), "admin.html")

        self.dashboard_counters = []

    def admin_checker(self, func):
        self.admin_checker_func = func

    def is_admin(self, user):
        if self.admin_checker_func:
            return self.admin_checker_func(user)
        return getattr(user, 'is_admin', False)

    def init_blueprints(self, app):
        self.register_blueprint(admin_bp)
        for feature in app.features:
            if hasattr(feature, "init_admin"):
                feature.init_admin(self, app)
        self.init_admin_signal.send(app, admin=self)

    def register_blueprint(self, bp):
        if isinstance(bp, str):
            bp = import_string(bp)
        self.app.register_blueprint(bp, **self.get_blueprint_options(bp))

    def get_blueprint_options(self, bp=None):
        url_prefix = self.options["url_prefix"]
        if bp and bp.url_prefix:
            url_prefix = (url_prefix + "/" + bp.url_prefix.lstrip("/")).rstrip("/")
        return dict(url_prefix=url_prefix, subdomain=self.options["subdomain"])

    def register_dashboard_counter(self, label, value_func, icon, color='blue'):
        self.dashboard_counters.append((label, icon, color, value_func))