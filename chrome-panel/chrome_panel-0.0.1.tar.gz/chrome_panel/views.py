from django.http import HttpResponse


# Create your views here.


def panels(request):
    """Render the contents of a panel"""
    # toolbar = DebugPanel.fetch(request.GET['store_id'])
    # if toolbar is None:
    #    content = _("Data for this panel isn't available anymore. "
    #                "Please reload the page and retry.")
    #    content = "<p>%s</p>" % escape(content)
    # else:
    #    panel = toolbar.get_panel_by_id(request.GET['panel_id'])
    #    content = panel.content
    return HttpResponse("")
