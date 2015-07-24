from DateTime import DateTime
from Zope2 import app
from zope.component.hooks import setSite
import os
from zope.component import getUtility
from Products.MailHost.interfaces import IMailHost
from zope.component.interfaces import ComponentLookupError


def get_plone_site(connection, plone_path=None):
    """ Return plone site """
    container = app()
    # app = container.unrestrictedTraverse('/')
    if plone_path:
        plone_paths = [path for path in plone_path.split(os.sep) if path]
        for path_name in plone_paths:
            container = container.get(path_name)
        plone_site = container
        if not plone_site:
            msg = "Error, path '{0}' do not exist".format(plone_path)
            connection.write(str(msg))
            return False
        if plone_site.meta_type != "Plone Site":
            msg = "Error, path {0} is not a plone site, it's {1}".format(plone_path, plone_site.meta_type)
            connection.write(str(msg))
            return False
        else:
            return plone_site
    else:
        result = False
        for obj in container.values():
            if obj.meta_type == "Folder":  # if plonesite come from mount point
                for plone in obj.values():
                    if plone.meta_type == "Plone Site":
                        result = plone
            else:
                if obj.meta_type == "Plone Site" and not result:
                    result = obj
        return result


def get_users(context, obj=True):
    from Products.CMFCore.utils import getToolByName
    portal = getToolByName(context, "portal_url").getPortalObject()
    users = []
    for user in portal.acl_users.searchUsers():
        if user['pluginid'] == 'source_users':
            if obj:
                users.append(portal.portal_membership.getMemberById(user['userid']))
            else:
                users.append(user['userid'])
    return users


def count_users(connection, plone_path=None):
    """the total amount of users in your plone site"""
    plone_site = get_plone_site(connection, plone_path)
    if plone_site:
        setSite(plone_site)
        users = get_users(plone_site)
        connection.write(str(len(users)))


def count_valid_users(connection, plone_path=None):
    """Count all users connected since 90 days"""
    plone_site = get_plone_site(connection, plone_path)
    if plone_site:
        setSite(plone_site)
        users = get_users(plone_site)
        valid_users = []
        for user in users:
            if user.getProperty("last_login_time") > (DateTime() - 90):
                valid_users.append(user)
        connection.write(str(len(valid_users)))


def check_smtp(connection, plone_path=None):
    """Check if SMTP is initialize, return number of errors found. """
    plone_site = get_plone_site(connection, plone_path)
    if plone_site:
        setSite(plone_site)
        try:
            mail_host = getUtility(IMailHost)
        except ComponentLookupError:
            mail_host = getattr(plone_site, "MailHost")
        mail_errors = []
        if not mail_host.smtp_host:
            mail_errors.append("incorrect host: {0}".format(mail_host.smtp_host))
        if mail_host.smtp_port != 25:
            mail_errors.append("incorrect port")
        if (hasattr(mail_host, "smtp_userid") and mail_host.smtp_userid) or (
                hasattr(mail_host, "smtp_uid") and mail_host.smtp_uid):
            mail_errors.append("user entered")
        if (hasattr(mail_host, "smtp_pass") and mail_host.smtp_pass) or (
                hasattr(mail_host, "smtp_pwd") and mail_host.smtp_pwd):
            mail_errors.append("password entered")
        if not plone_site.email_from_address or plone_site.email_from_address == "postmaster@localhost":
            mail_errors.append("bad mail")
        connection.write(str(len(mail_errors)))


def check_upgrade_steps(connection, plone_path=None):
    """Check if all upgrade steps are ran."""
    plone_site = get_plone_site(connection, plone_path)
    not_upgraded = 0
    if plone_site:
        setSite(plone_site)
        ps = plone_site.portal_setup
        # qit = plone_site.portal_quickinstaller
        for profile_id in ps.listProfilesWithUpgrades():
            is_installed = ps.getLastVersionForProfile(profile_id) != 'unknown'
            if is_installed:
                # latest_upgrade_step = qit.getLatestUpgradeStep(profile_id)
                # if latest_upgrade_step != 'unknown':
                upgrades = ps.listUpgrades(profile_id)
                if upgrades:
                    not_upgraded += 1

        connection.write(str(not_upgraded))


def last_login_time(conn, plone_path=None):
    """Get last login time user"""
    plone_site = get_plone_site(conn, plone_path)
    if plone_site:
        setSite(plone_site)
        users = get_users(plone_site)
        last_login = ""
        for user in users:
            if not last_login:
                last_login = user.getProperty("last_login_time")
            if user.getProperty("last_login_time") > last_login:
                last_login = user.getProperty("last_login_time")
        conn.write(str(last_login))


def creation_date_plonesite(conn, plone_path=None):
    """Get creation date of plonesite object"""
    plone_site = get_plone_site(conn, plone_path)
    if plone_site:
        setSite(plone_site)
        creation_date = plone_site.creation_date.Date()
    conn.write(str(creation_date))
