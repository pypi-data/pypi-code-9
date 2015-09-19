"""
WebPortfolio command line tool

manage.py

Command line tool to manage your application

"""

import argparse
from application import get_config
import application.model as model
from webportfolio import utils

from webportfolio.module import user

config = get_config()
NAME = "WebPortfolio Manager"
__version__ = 1#config.APP_VERSION


def setup():

    # Create all db
    model.db.create_all()

    # :: USERS
    # Setup primary roles.
    # PRIMARY ROLES is a set of tuples [(level, name), ...]
    [model.User.Role.new(level=r[0], name=r[1]) for r in user.PRIMARY_ROLES]

    # ADD SUPER ADMIN
    email = config.ADMIN_EMAIL
    name = config.ADMIN_NAME
    if utils.is_valid_email(email):
        user = model.User.User.get_by_email(email)
        if not user:
            model.User.User.new(email=email, name=name, role="SUPERADMIN")
    else:
        raise AttributeError("Couldn't create new SUPERADMIN. 'email' is invalid")

    # :: POSTS
    # Set types
    post_types = ["Blog", "Article", "Page", "Other"]
    if not model.Cms.Type.all().count():
        [model.Cms.Type.new(t) for t in post_types]

    # Set categories
    post_categories = ["Blog"]
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

def main():
    parser = argparse.ArgumentParser(description="%s  v.%s" % (NAME, __version__))
    parser.add_argument("--setup", help="Setup the system",  action="store_true")
    parser.add_argument("--upload-assets-to-s3", help="Upload all webportfolio files to S3", action="store_true")
    parser.add_argument("--assets", help="Assets",  action="store_true")
    arg = parser.parse_args()

    if arg.setup:
        # Default setup
        print("Setting up...")
        setup()

    if arg.upload_assets_to_s3:
        # Upload webportfolio files to s3
        from run_www import app
        #import flask_s3
        #import run_www  # Or the main application run file
        #print("Upload webportfolio files to S3")
        #flask_s3.create_all(run_www.app)
        print 1

    if arg.assets:

        print "Done"

from run_www import app
from flask.ext.script import Manager , Shell, Server
manager = Manager(app, with_default_commands=False)

@manager.command
def setup():
    """
    To setup a script
    """
    print "SETUP DONE!"

    print ("Hello World")

if __name__ == "__main__":
    from flask_assets import ManageAssets
    manager.add_command("assets", ManageAssets())

    manager.run()


