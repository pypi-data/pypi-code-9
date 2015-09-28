
from webportfolio import WebPortfolio

WebPortfolio.register_module(__name__)

def view(template_dir=None):
    """
    Create the Error view
    Must be instantiated

    import error_view
    ErrorView = error_view()

    :param template_dir: The directory containing the view pages
    :return:
    """
    if not template_dir:
        template_dir = "WebPortfolio/Module/ErrorPage"

    template_page = "%s/index.html" % template_dir

    class Error(WebPortfolio):
        """
        Error Views
        """
        @classmethod
        def register(cls, app, **kwargs):
            super(cls, cls).register(app, **kwargs)

            @app.errorhandler(400)
            def error_400(error):
                return cls.index(error, 400)

            @app.errorhandler(401)
            def error_401(error):
                return cls.index(error, 401)

            @app.errorhandler(403)
            def error_403(error):
                return cls.index(error, 403)

            @app.errorhandler(404)
            def error_404(error):
                return cls.index(error, 404)

            @app.errorhandler(500)
            def error_500(error):
                return cls.index(error, 500)

            @app.errorhandler(503)
            def error_503(error):
                return cls.index(error, 503)

        @classmethod
        def index(cls, error, code):
            cls.page_meta(title="Error %s" % code)

            return cls.render(error=error, view_template=template_page), code
    return Error

ErrorV = view()