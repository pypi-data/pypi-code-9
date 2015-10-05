
"""
Contact Page
"""

from flask import request, redirect, url_for, abort
from webportfolio import (WebPortfolio, route, mailer, recaptcha, nav_menu,
                       flash_error, flash_success, warn_missing_config)
import webportfolio.utils as utils

WebPortfolio.register_module(__name__)

def contact_page(view, **kwargs):
    """
    :param view: The view to copy to
    :param kwargs:
        - fa_icon
        - menu: The name of the menu
        - show_menu: bool - show/hide menu
        - menu_order: int - position of the menu
    :return:
    """
    opt_route = kwargs.pop("route", {})
    opt_nav_menu = kwargs.pop("nav_menu", {})

    template_dir = kwargs.pop("template_dir", "WebPortfolio/Module/ContactPage")
    template_page = template_dir + "/%s.html"

    @nav_menu(kwargs.get("menu", "Contact"),
              order=kwargs.get("menu_order", 100),
              fa_icon=kwargs.get("fa_icon"),
              show=True if kwargs.get("show_menu") is None else kwargs.get("show_menu"),
              endpoint="ContactPage",
              __is_class=False,
              __module=view.__module__,
              __class=view.__name__

              )
    @route("contact", methods=["GET", "POST"], endpoint="ContactPage")
    def contact_page(self):
        if not self.config("MAILER_URI") \
                or not self.config("MODULE_CONTACT_PAGE_EMAIL"):
            abort(500, "Mailer Error. Invalid [ MAILER_URI ] "
                       "or [ MODULE_CONTACT_PAGE_EMAIL ] is missing or empty")

        contact_email = self.config("MODULE_CONTACT_PAGE_EMAIL")

        if request.method == "POST":
            error_message = None
            email = request.form.get("email")
            subject = request.form.get("subject")
            message = request.form.get("message")
            name = request.form.get("name")

            if recaptcha.verify():
                if not email or not subject or not message:
                    error_message = "All fields are required"
                elif not utils.is_valid_email(email):
                    error_message = "Invalid email address"
                if error_message:
                    flash_error(error_message)
                else:
                    mailer.send_template("contact-us.txt",
                                         to=contact_email,
                                         reply_to=email,
                                         mail_from=email,
                                         mail_subject=subject,
                                         mail_message=message,
                                         mail_name=name
                                        )
                    flash_success("Message sent. Thank you!")
            else:
                flash_error("Security code is invalid")
            return redirect(url_for("ContactPage"))
        else:
            self.page_meta(title="Contact Us")
            return self.render(view_template=template_page % "contact_page")

    return contact_page


