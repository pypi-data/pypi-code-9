class Bull:
    '''
    Class Bull represents bullet
    '''
    def __init__(self, start, target, power):
        '''
        Initialize bullet
        @param start: start point
        @param target: target
        @param power: power of bullet
        '''
        self.start = start
        self.target = target
        self.position = start
        self.power = power

    def getStart(self):
        '''
        Get start point of bullet
        @return: start point
        '''
        return self.start

    def getTarget(self):
        '''
        Get bullet's target
        @return: target
        '''
        return self.target

    def getPosition(self):
        '''
        Get bullet's current position
        @return: current position
        '''
        return self.position

    def setPosition(self, position):
        '''
        Set bullet's position
        @param position: position
        '''
        self.position = position

    def getPower(self):
        '''
        Get bullet's power
        @return: power
        '''
        return self.power
