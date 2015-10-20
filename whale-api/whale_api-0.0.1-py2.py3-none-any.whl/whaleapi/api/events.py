from whaleapi.api.base import SendableAPIResource


class Event(SendableAPIResource):
    class_name = 'event'
    class_url = '/events'
    plural_class_name = 'events'
    json_name = 'event'

    @classmethod
    def send(cls, events=None, **single_event):

        if events:
            events_dict = {"events": events}
        else:
            events = [single_event]
            events_dict = {"events": events}

        return super(Event, cls).send(**events_dict)
