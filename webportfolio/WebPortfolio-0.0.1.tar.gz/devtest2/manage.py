"""
WebPortfolio command line tool

manage.py

Command line tool to manage your application

"""

from webportfolio import get_env_config
import webportfolio.utils
from flask.ext.script import Manager

import run_www
from application import config, model
from webportfolio.module.user import PRIMARY_ROLES as USER_PRIMARY_ROLES

manager = Manager(run_www.app, with_default_commands=False)

conf = get_env_config(config)

NAME = "WebPortfolio Manager"


@manager.command
def setup():
    """
    Setup
    :return:
    """

    # Create all db
    model.db.create_all()

    # :: USERS
    # Setup primary roles.
    # PRIMARY ROLES is a set of tuples [(level, name), ...]
    [model.User.Role.new(level=r[0], name=r[1]) for r in USER_PRIMARY_ROLES]

    # ADD SUPER ADMIN
    if not hasattr(conf, "APPLICATION_ADMIN_EMAIL") \
        or not conf.APPLICATION_ADMIN_EMAIL \
        or conf.APPLICATION_ADMIN_EMAIL == "" \
        or not webportfolio.utils.is_valid_email(conf.APPLICATION_ADMIN_EMAIL):
        raise AttributeError("APPLICATION_ADMIN_EMAIL is empty or not valid" )
    else:
        admin_email = conf.APPLICATION_ADMIN_EMAIL
        user = model.User.User.get_by_email(admin_email)
        if not user:
            model.User.User.new(email=admin_email, name="ADMIN", role="superadmin")

    # :: POSTS
    # Set types
    post_types = ["Page", "Blog", "Article", "Other"]
    if not model.Cms.Type.all().count():
        [model.Cms.Type.new(t) for t in post_types]

    # Set categories
    post_categories = ["Uncatgorized"]
    if not model.Cms.Category.all().count():
        [model.Cms.Category.new(c) for c in post_categories]

    posts = [
        {
            "title": "About Us",
            "slug": "about",
            "type": "Page"
        },
        {
            "title": "Terms of Service",
            "slug": "tos",
            "type": "Page"
        }
    ]

if __name__ == "__main__":
    print("WebPortfolio Manager")

    manager.run()


