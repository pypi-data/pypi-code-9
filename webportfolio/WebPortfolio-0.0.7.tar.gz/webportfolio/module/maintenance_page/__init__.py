
from webportfolio import WebPortfolio, logger

WebPortfolio.register_module(__name__)

def view(template=None):
    """
    Create the Maintenance view
    Must be instantiated

    import maintenance_view
    MaintenanceView = maintenance_view()

    :param view_template: The directory containing the view pages
    :return:
    """
    if not template:
        template = "WebPortfolio/Module/MaintenancePage/index.html"

    class Maintenance(WebPortfolio):
        @classmethod
        def register(cls, app, **kwargs):
            super(cls, cls).register(app, **kwargs)

            if cls.config("MODULE_MAINTENANCE_PAGE_ON"):
                logger.info("MAINTENANCE PAGE IS ON")

                @app.before_request
                def on_maintenance():
                    return cls.render(layout=template), 503

    return Maintenance

Maintenance = view()