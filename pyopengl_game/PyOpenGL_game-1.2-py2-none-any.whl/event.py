EVENT_WAVE_TIMER = 0
EVENT_ENEMY = 1
EVENT_DELAY = 2


class Event:
    '''
    Class Event represents game event such as enemy spawning, delay and new wave
    '''
    def __init__(self, type, object):
        '''
        Initialize event
        @param type: event type
        @param object: event object
        '''
        self.type = type
        self.object = object

    def getType(self):
        '''
        Get type of event
        @return: event type
        '''
        return self.type

    def getObject(self):
        '''
        Get event object
        @return: event object
        '''
        return self.object
