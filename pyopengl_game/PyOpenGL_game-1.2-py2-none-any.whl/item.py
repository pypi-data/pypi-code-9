COLOR_RED = 0
COLOR_BLUE = 1
COLOR_GREEN = 2


class Item:
    '''
    Class Item represent flyint item.
    '''
    def __init__(self, position, color, count):
        '''
        Initialize flying item
        @param position: position
        @param color: color
        @param count: item count when picked up
        @return:
        '''
        # Initialize members
        self.position = position
        self.color = color
        self.count = count
        self.lifetime = 1.0

    def getPosition(self):
        '''
        Get item position
        @return: item position
        '''
        return self.position

    def setPosition(self, position):
        '''
        Set item position
        @param position: position
        '''
        self.position = position

    def getColor(self):
        '''
        Get item color
        @return: item color
        '''
        return self.color

    def setColor(self, color):
        '''
        Set item color
        @param color: color
        '''
        self.color = color

    def getCount(self):
        '''
        Get item count
        @return: item count
        '''
        return self.count

    def setCount(self, count):
        '''
        Set item count
        @param count: count
        '''
        self.count = count

    def getLifetime(self):
        '''
        Get item lifetime
        @return: item lifetime
        '''
        return self.lifetime

    def setLifetime(self, lifetime):
        '''
        Set item lifetime
        @param lifetime: lifetime
        '''
        self.lifetime = lifetime
