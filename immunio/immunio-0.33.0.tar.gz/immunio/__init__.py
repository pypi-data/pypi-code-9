from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from pkg_resources import resource_filename


__agent_name__ = "agent-python"
__version__ = "0.33.0"
__vm_version__ = "2.2.0"


__ca_file__ = resource_filename(__name__, "immunio_ca.crt")


# Hold singleton copies of key objects for this app
_global_config = None
_global_plugin_manager = None
_global_agent = None


def auto_start():
    """
    Called automatically if you `import immunio.start`. Loads the agent
    config and does the MonkeyPatching. The agent will be created and
    started automatically on the first request.
    """
    config = get_config()
    if not config.agent_enabled:
        # If agent is not enabled, do nothing
        return
    # Do MonkeyPatching
    get_plugin_manager()


def get_config():
    """
    Load the Agent Config into a singleton.
    """
    from immunio.config import Config
    global _global_config

    if not _global_config:
        _global_config = Config()
    return _global_config


def get_plugin_manager():
    """
    Load PluginManager into a singleton and actually do the MonkeyPatching.
    """
    from immunio.plugin_manager import PluginManager
    global _global_plugin_manager

    if not _global_plugin_manager:
        config = get_config()
        _global_plugin_manager = PluginManager(config, get_agent_func=get_agent)
    return _global_plugin_manager


def get_agent():
    """
    Shortcut function for accessing a singleton agent.
    """
    # Import inside function to avoid circular import.
    from immunio import agent
    global _global_agent

    if not _global_agent:
        _global_agent = agent.Agent(get_config(), get_plugin_manager())
        _global_agent.start()
    return _global_agent


def start():
    """
    Manual function to create an agent and start it up. Returns
    a reference to the agent so it can be used in a call to
    `agent.wrap_wsgi_app(original_app)`.

    This is only required for frameworks where we don't automatically wrap
    the produced wsgi app. In most cases you should just
    `import immunio.start` at the top of your application entry file.
    """
    return get_agent()


def report_failed_login_attempt(username, reason=None):
    """
    Inform Immunio of a failed login attempt.
    """
    global _global_agent
    # If we don't have an enabled agent, do nothing.
    if not _global_agent or not _global_agent.enabled:
        return

    _global_agent.run_hook("immunio_api", "authenticate", {
        "is_valid": False,
        "username": username,
        "reason": reason,
    })


def report_custom_threat(threat_name, message, metadata=None):
    """
    Inform Immunio of custom threat for your app.
    """
    global _global_agent
    # If we don't have an enabled agent, do nothing.
    if not _global_agent or not _global_agent.enabled:
        return

    if not (isinstance(threat_name, str) or isinstance(threat_name, unicode)):
        raise ValueError(
            "`threat_name` must be str or unicode, not %r" % threat_name)

    if not (isinstance(message, str) or isinstance(message, unicode)):
        raise ValueError(
            "`message` must be str or unicode, not %r" % message)

    if metadata is None:
        metadata = {}

    if not isinstance(metadata, dict):
        raise ValueError("`metadata` must be a dict, not %r" % metadata)

    _global_agent.run_hook("immunio_api", "custom_threat", {
        "threat_name": threat_name,
        "message": message,
        "display_meta": metadata,
    })
