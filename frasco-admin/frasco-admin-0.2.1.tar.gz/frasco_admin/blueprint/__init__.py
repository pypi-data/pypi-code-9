from ..view import AdminBlueprint
from frasco import current_context


admin_bp = AdminBlueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin_bp.view("/", template="admin/dashboard.html", admin_title="Dashboard",
    admin_menu="Dashboard", admin_menu_icon="tachometer")
def dashboard():
    pass