import os

execfile(os.environ.get('SLACK_RTM_BOT_SETTINGS_FILE', os.path.join(
    os.path.dirname(__file__), 'settings_local.py')))
