"""
WebPortfolio

Your views

"""

from flask import redirect, request, url_for, session, jsonify
from webportfolio import (WebPortfolio, route, extends, nav_menu,
                       mailer, cache, storage, recaptcha, csrf,
                       user_authenticated, user_not_authenticated, user_roles,
                       flash_error, flash_success, flash_info, flash_data, get_flashed_data,
                       ModelError, ViewError)

from webportfolio.module import contact_page
from application import model

@nav_menu("Home", key="Main", order=1)
@extends(contact_page.user)
class Index(WebPortfolio):
    route_base = "/"

    def index(self):
        self.page_meta(title="Hello WebPortfolio!")
        return self.render()


