"""
WebPortfolio command line tool

manage.py

Command line tool to manage your application

"""

import click
from webportfolio import get_env_config
import webportfolio.utils

from application import config, model
from webportfolio.module.user import PRIMARY_ROLES as USER_PRIMARY_ROLES

conf = get_env_config(config)

@click.group()
def cli():
    pass

@cli.command()
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
        raise Exception("APPLICATION_ADMIN_EMAIL is empty or not valid")
    else:
        random_password = webportfolio.utils.generate_random_string()
        admin_email = conf.APPLICATION_ADMIN_EMAIL
        user = model.User.User.get_by_email(admin_email)
        if not user:
            model.User.User.new(email=admin_email,
                                password=random_password,
                                first_name="Admin",
                                role="superadmin")
            click.echo("")
            click.echo("** New Super Admin Created")
            click.echo("- Admin Email: %s" % admin_email)
            click.echo("- Admin Password: %s" % random_password)
            click.echo("")

    # :: POSTS
    # Set types
    post_types = ["Page", "Blog", "Document", "Other"]
    if not model.Cms.Type.all().count():
        click.echo(" Creating CMS Post Types...")
        [model.Cms.Type.new(t) for t in post_types]

    # Set categories
    post_categories = ["Uncatgorized"]
    if not model.Cms.Category.all().count():
        click.echo(" Creating CMS Post Categories...")
        [model.Cms.Category.new(c) for c in post_categories]

    # Add some basic post
    if not model.Cms.Post.all().count():
        click.echo(" Creating standard CMS Posts...")
        user = model.User.User.get_by_email(admin_email)
        if not user:
            raise Exception("Can't insert new Posts. User doesn't exist")
        posts = [
            {
                "title": "About Us",
                "slug": "about",
                "content": "**About Us**",
                "type_slug": "document",
                "is_published": True,
                "user_id": user.id,
            },
            {
                "title": "Terms of Service",
                "slug": "tos",
                "content": "**Terms of Service**",
                "type_slug": "document",
                "is_published": True,
                "user_id": user.id,
            },
            {
                "title": "Privacy",
                "slug": "privacy",
                "content": "**Privacy Policy**",
                "type_slug": "document",
                "is_published": True,
                "user_id": user.id,
            },
            {
                "title": "First Page",
                "slug": "first-page",
                "content": "**This is our First Page!**",
                "type_slug": "page",
                "is_published": True,
                "user_id": user.id,
            },
            {
                "title": "First Blog",
                "slug": "first-blog",
                "content": "**This is our First Blog!**",
                "type_slug": "blog",
                "is_published": True,
                "user_id": user.id,
            }
        ]
        [model.Cms.Post.new(**post) for post in posts]

if __name__ == "__main__":
    click.echo("WebPortfolio Manager")

    cli()


