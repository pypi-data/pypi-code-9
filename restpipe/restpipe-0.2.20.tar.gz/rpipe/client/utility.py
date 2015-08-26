import rpipe.config.client
import rpipe.utility


_CLIENT_EVENT_HANDLER = None
def get_client_event_handler():
    global _CLIENT_EVENT_HANDLER

    if _CLIENT_EVENT_HANDLER is None:
        event_handler_cls = \
            rpipe.utility.load_cls_from_string(
                rpipe.config.client.EVENT_HANDLER_FQ_CLASS)

        assert issubclass(event_handler_cls, ClientEventHandler) is True

        _CLIENT_EVENT_HANDLER = event_handler_cls()

    return _CLIENT_EVENT_HANDLER
