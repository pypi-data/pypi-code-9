"""
Shortcut module to automatically start a new Immunio Agent.

Add `import immunio.start` to the top of your app's entrypoint and this will
automatically monkeypatch the required libraries, start the Agent when
a new WSGI app is created, and wrap the WSGI callable.
"""
import immunio

# Load the config and do MonkeyPatching.
immunio.auto_start()
