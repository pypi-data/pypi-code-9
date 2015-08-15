from numpy import *


class Player:
    '''
    Class Player represents player or enemy
    '''

    def __init__(self, power = 1, defence = 1, speed = 1):
        '''
        Initialize
        @param power: power
        @param defence: defenct
        @param speed: speed
        '''
        # Initialize members
        self.position = array([0, 0, 0], 'f')
        self.red_items = 0
        self.blue_items = 0
        self.green_items = 0
        self.power = power
        self.defence = defence
        self.speed = speed
        self.reload = 0.0
        self.health = 1.0
        self.stamina = 0.0

    def getPosition(self):
        '''
        Get position
        @return: position
        '''
        return self.position

    def setPosition(self, position):
        '''
        Set position
        @param position: position
        '''
        self.position = position

    def getRedItems(self):
        '''
        Get red items count
        @return: red items count
        '''
        return self.red_items

    def setRedItems(self, red_items):
        '''
        Set red items count
        @param red_items: red items count
        '''
        self.red_items = red_items

    def addRedItems(self, red_items):
        '''
        Add red items
        @param red_items: red items count
        '''
        self.red_items += red_items

    def getBlueItems(self):
        '''
        Get blue items count
        @return: blue items count
        '''
        return self.blue_items

    def setBlueItems(self, blue_items):
        '''
        Set blue items count
        @param blue_items: blue items count
        '''
        self.blue_items = blue_items

    def addBlueItems(self, blue_items):
        '''
        Add blue items
        @param blue_items: blue items count
        '''
        self.blue_items += blue_items

    def getGreenItems(self):
        '''
        Get green items count
        @return: green items count
        '''
        return self.green_items

    def setGreenItems(self, green_items):
        '''
        Set green items count
        @param green_items: green items count
        '''
        self.green_items = green_items

    def addGreenItems(self, green_items):
        '''
        Add green items
        @param green_items: green items count
        '''
        self.green_items += green_items

    def getPower(self):
        '''
        Get power
        @return: power
        '''
        return self.power

    def setPower(self, power):
        '''
        Set power
        @param power: power
        '''
        self.power = power

    def addPower(self, power):
        '''
        Add power
        @param power: power
        '''
        self.power += power

    def getDefence(self):
        '''
        Get defence
        @return: defence
        '''
        return self.defence

    def setDefence(self, defence):
        '''
        Set defence
        @param defence: defence
        '''
        self.defence = defence

    def addDefence(self, defence):
        '''
        Add defence
        @param defence: defence
        '''
        self.defence += defence

    def getSpeed(self):
        '''
        Get speed
        @return: speed
        '''
        return self.speed

    def setSpeed(self, speed):
        '''
        Set speed
        @param speed: speed
        '''
        self.speed = speed

    def addSpeed(self, speed):
        '''
        Add speed
        @param speed: speed
        '''
        self.speed += speed

    def getReload(self):
        '''
        Get reload counter
        @return: reload counter
        '''
        return self.reload

    def setReload(self, reload):
        '''
        Set reload counter
        @param reload: reload counter
        '''
        self.reload = reload

    def getHealth(self):
        '''
        Get health
        @return: health
        '''
        return self.health

    def setHealth(self, health):
        '''
        Set health
        @param health: health
        '''
        self.health = health

    def getStamina(self):
        '''
        Get stamina
        @return: stamina
        '''
        return self.stamina

    def setStamina(self, stamina):
        '''
        Set stamina
        @param stamina: stamina
        '''
        self.stamina = stamina

    def addStamina(self, stamina):
        '''
        Add stamina
        @param stamina: stamina
        '''
        self.stamina += stamina
