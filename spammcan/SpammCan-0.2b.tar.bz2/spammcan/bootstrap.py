"""Functions for bootstrapping the database used by the commands module."""

__all__ = [
    'bootstrap_model',
    'create_formats',
    'create_tables',
    'create_default_user'
]

from getpass import getpass

from turbogears.database import get_engine, session
from spammcan.model import metadata, Format, Style, User

# functions for populating the database

def bootstrap_model(clean=False, create_user=False):
    """Create all database tables and fill them with default data."""
    create_tables(clean)
    create_formats()
    create_styles()
    if create_user:
        create_default_user(options.user)

def create_default_user(user_name):
    """Create a default user."""
    try:
        u = User.by_user_name(user_name)
    except:
        u = None
    if u:
        print _(u"User '%s' already exists in database.") % user_name
        return
    while True:
        password = getpass(_(u"Enter password for user '%s': ") % user_name).strip()
        password2 = getpass(_(u"Confirm password: ")).strip()
        if password != password2:
            print _(u"Passwords do not match.")
        else:
            break
    u = User(user_name=user_name, display_name=u"Default User",
        email_address=u"%s@nowhere.xyz" % user_name, password=password)
    session.save(u)
    session.flush()
    print _(u"User '%s' created.") % user_name

def create_formats():
    """Populate the 'format' table."""
    from pygments.lexers import get_all_lexers

    if Format.query().count():
        return
    lexers = sorted(get_all_lexers(), key=lambda k: k[0].lower())
    for name, aliases, extensions, mimetypes in lexers:
        f = Format(name=aliases[0], display_name=unicode(name))
        session.save(f)
    session.flush()
    print _(u"Populated 'format' table.")

def create_styles():
    """Populate the 'style' table."""
    from pygments.styles import get_all_styles

    if Style.query().count():
        return
    styles = sorted(get_all_styles(), key=lambda k: k[0].lower())
    for name in styles:
        s = Style(name=name, display_name=unicode(name.capitalize()))
        session.save(s)
    session.flush()
    print _(u"Populated 'style' table.")

def create_tables(drop_all=False):
    """Create all tables defined in the model in the database.

    Optionally drop existing tables before creating them.

    """
    if drop_all:
        print "Dropping all database tables defined in model."
    metadata.bind = get_engine()
    if drop_all:
        metadata.drop_all()
    metadata.create_all()
    print _(u"All database tables defined in model created.")
