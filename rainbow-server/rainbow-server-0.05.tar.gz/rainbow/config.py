g_CONFIG = {}

g_Online_Server = {}
# g_Online_Server_List = []

from collections import deque
g_Online_Server_deque = deque()


# invalid code and message
RAINBOW_INVALID_CODE_MSG = {
    '60001': 'invalid signature',
    '60002': 'identity is required',
    '60003': 'POST method is required',
}
