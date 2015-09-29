"""
WebPortfolio View
"""
from flask import redirect, request, url_for, session, jsonify
from webportfolio import (WebPortfolio, route, extends, nav_menu,
                       mailer, cache, storage, recaptcha, csrf,
                       with_user_roles, login_required, no_login_required,
                       flash_error, flash_success, flash_info, flash_data, get_flashed_data,
                       ModelError, ViewError)
from webportfolio.module import contact_page, user, cms
from application import model


# ------------------------------------------------------------------------------
# /
# This is the entry point of the site
# All root based (/) endpoint could be placed in here
#
# It extends the contact_page module, to be accessed at '/contact'
#
@extends(contact_page.contact_page)
class Index(WebPortfolio):
    route_base = "/"

    @nav_menu("Home", order=1)
    def index(self):
        self.page_meta(title="Hello WebPortfolio!")
        return self.render()

# ------------------------------------------------------------------------------
# /admin
# This is the admin view
# It extends the 'cms.admin' module to manage posts
# It extends the 'user.admin' module to manage users
#
@nav_menu("Admin", group="admin")
@extends(cms.admin, model=model)
@extends(user.admin, model=model)
class Admin(WebPortfolio):
    LAYOUT = "admin-layout.html"
    route_base = "admin"
    decorators = [with_user_roles('superadmin', 'admin')]

    @nav_menu("Home")
    def index(self):
        self.page_meta(title="My Admin Home Page")
        return self.render()

    @nav_menu("Page 2")
    def page_2(self):
        self.page_meta(title="My 2nd Page")
        return self.render()

# ------------------------------------------------------------------------------
# /account
# This is a User Account section
# It extends the 'user.account' module, which automatically requires the
# endpoint to be authenticated
# If you don't an endpoint to be authenticated, just at the decorator:
# '@no_login_required'
#
@nav_menu("My Account", group="account", order=3, align_right=True)
@extends(user.account, model=model)
class Account(WebPortfolio):

    @nav_menu("My Account", order=1)
    def index(self):
        self.page_meta(title="My Account")
        return self.render()

    @nav_menu("Upload Image Demo", order=2)
    @route("upload", methods=["GET", "POST"])
    def upload(self):

        self.page_meta(title="Upload Demo")

        if request.method == "POST":
            try:
                _file = request.files.get('file')
                if _file:
                    my_object = storage.upload(_file,
                                               prefix="demo/",
                                               public=True,
                                               allowed_extensions=["gif", "jpg", "jpeg", "png"])
                    if my_object:
                        return redirect(url_for("Account:upload", object_name=my_object.name))
            except Exception as e:
                flash_error(e.message)
            return redirect(url_for("Account:upload"))

        my_object = None
        object_name = request.args.get("object_name")
        if object_name:
            my_object = storage.get(object_name=object_name)

        return self.render(my_object=my_object)

    @nav_menu("No Login", order=3)
    @no_login_required
    def no_login(self):
        self.page_meta(title="No Login")
        return self.render()

# ------------------------------------------------------------------------------
# /blog
# This a blog endpoint
# It extends the 'cms.post' module to fetch posts with 'blog' category
#
@extends(cms.post,
         model=model,
         query={
             "types": ["blog"],
             "order_by": "published_at desc",
         },
         endpoints={
             "index": {"menu": "Blog", "endpoint": "/", "per_page": 10,
                       "post_title": "My Blog",
                       "post_header": "My Blog",
                       "post_subheader": ""},
             "single": {"menu": "Read", "endpoint": "/:slug"},
             "authors": {"menu": "Authors", "endpoint": "authors", "show_menu": False},
             "archive": {"menu": "Archive", "endpoint": "archive", "show_menu": False},
         })
class Blog(WebPortfolio):
    pass



# ------------------------------------------------------------------------------
# /page
# This a blog endpoint
# It extends the 'cms.post' module to fetch posts with 'page' category
#
@extends(cms.post,
         model=model,
         query={
             "types": ["page"],
             "order_by": "title asc"
         },
         endpoints={
             "index": {"menu": "Pages",
                       "endpoint": "/",
                       "post_title": "Pages",
                       "post_show_byline": False},
             "single": {"menu": "Documents", "endpoint": "/:slug", "post_show_byline": False},
             "archive": {"menu": "Archive", "endpoint": "archive", "show_menu": False},
             "authors": {"menu": "Authors", "endpoint": "authors", "show_menu": False}
         })
class Page(WebPortfolio):
    pass


# ------------------------------------------------------------------------------
# /docs
# This a blog endpoint
# It extends the 'cms.post' module to fetch posts with 'document' category
#
@extends(cms.post,
         model=model,
         query={
             "types": ["document"],
             "order_by": "title asc"
         },
         endpoints={
             "index": {"menu": "Documents",
                       "endpoint": "/",
                       "post_title": "Documents",
                       "post_show_byline": False},
             "single": {"menu": "Documents", "endpoint": "/:slug", "post_show_byline": False},
             "archive": {"menu": "Archive", "endpoint": "archive", "show_menu": False},
             "authors": {"menu": "Authors", "endpoint": "authors", "show_menu": False}
         })
class Document(WebPortfolio):
    route_base = "docs"
