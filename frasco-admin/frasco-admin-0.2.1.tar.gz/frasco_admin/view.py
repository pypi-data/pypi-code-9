from frasco import Blueprint, current_context, pass_feature, ActionsView, hook, current_app, abort
import inflection


class AdminView(ActionsView):
    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop("admin_title", None)
        self.description = kwargs.pop("admin_desc", None)
        self.sidebar_menu = kwargs.pop("admin_menu", None)
        self.sidebar_menu_icon = kwargs.pop("admin_menu_icon", None)
        super(AdminView, self).__init__(*args, **kwargs)

    def register(self, target):
        if self.sidebar_menu:
            endpoint = self.name
            if isinstance(target, Blueprint):
                endpoint = target.name + "." + self.name
            current_app.features.menu["admin"].add_child(endpoint, self.sidebar_menu,
                endpoint, icon=self.sidebar_menu_icon)
        super(AdminView, self).register(target)

    def dispatch_request(self, *args, **kwargs):
        current_context["admin_section_title"] = self.title or inflection.humanize(self.name)
        current_context["admin_section_desc"] = self.description
        return super(AdminView, self).dispatch_request(*args, **kwargs)


class AdminBlueprint(Blueprint):
    view_class = AdminView

    def __init__(self, *args, **kwargs):
        super(AdminBlueprint, self).__init__(*args, **kwargs)

    def is_user_allowed(self, user):
        return True

    @hook('before_request')
    @pass_feature("admin", "users")
    def init_admin(self, admin, users):
        users.login_required()
        if not admin.is_admin(users.current) or not self.is_user_allowed(users.current):
            abort(404)
