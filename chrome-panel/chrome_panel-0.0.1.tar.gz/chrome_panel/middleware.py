import threading
from chrome_panel.panel import DebugPanel


class ChromePanelMiddleware(object):
    debug_panel = {}

    def process_request(self, request):
        # Decide whether the toolbar is active for this request.
        # if not self.show_toolbar(request):
        #    print("dont show toolbar")
        #    return

        toolbar = DebugPanel(request, threading.current_thread().ident)
        self.__class__.debug_panel[threading.current_thread().ident] = toolbar

        # Run process_request methods of panels like Django middleware.
        response = None
        for panel in toolbar.enabled_panels:
            response = panel.process_request(request)
            if response:
                break
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        toolbar = self.__class__.debug_panel.get(threading.current_thread().ident)
        if not toolbar:
            return

        # Run process_view methods of panels like Django middleware.
        response = None
        for panel in toolbar.enabled_panels:
            response = panel.process_view(request, view_func, view_args, view_kwargs)
            if response:
                break
        return response

    def process_response(self, request, response):
        toolbar = self.__class__.debug_panel.pop(threading.current_thread().ident, None)
        if not toolbar:
            return response

        # Run process_response methods of panels like Django middleware.
        for panel in reversed(toolbar.enabled_panels):
            new_response = panel.process_response(request, response)
            if new_response:
                response = new_response

        response['X-CHROME-PANEL'] = toolbar.render_toolbar()

        return response
