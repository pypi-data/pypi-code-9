"""

"""
from wagtail.wagtailadmin.edit_handlers import ObjectList


def add_panel_to_edit_handler(model, panel_cls, heading):
    """

    """
    from wagtail.wagtailadmin.views.pages import get_page_edit_handler

    edit_handler = get_page_edit_handler(model)
    edit_handler.children.append(ObjectList(
        [panel_cls(),],
        heading = heading
    ).bind_to_model(model))
