from __future__ import absolute_import

# importing on the yun requires the try block, importing on a desktop
# system works with the except block (?!)
try:
    from websocket import websocket

    from websocket.websocket import WebSocketConnectionClosedException
except ImportError:
    import websocket

    from websocket import WebSocketConnectionClosedException
