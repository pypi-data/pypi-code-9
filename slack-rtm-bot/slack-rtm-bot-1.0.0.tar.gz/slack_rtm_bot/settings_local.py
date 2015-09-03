import logging
import os

API_TOKEN = os.environ.get('SLACK_RTM_BOT_API_TOKEN')

LOG_FILE = None
LOG_FORMAT = '%(asctime)s: %(levelname)s: %(message)s'
LOG_LEVEL = logging.INFO

READ_INTERVAL_SECONDS = 1.0

# OwnerHandler
CHANNEL_OWNERS = {}

# ReactionHandler
EMOJI_REACTIONS = {}
