#-*- coding: utf-8 -*-

import httplib, urllib, urllib2, json

class blueskyconn:
    global createBlueskyParam
    global login
    global logout
    global blueskyGet
    global sensornetwork

    # blueskyGateway should not be included the protocol identifier like [http://].
    # Warnning: We suggest you to using the plubic account of bluesky here.
    def __init__(self, blueskyGateway, username, password):
        self.blueskyGateway = blueskyGateway.replace("http://", "")
        self.username = username
        self.password = password

    # Using sensornetwork with bluesky API.
    def sensornetwork(self, opts):
        params = createBlueskyParam(self, "sensornetwork", opts)
        #print "-------------------"
        #print params
        #print "-------------------"
        doTheAPI = blueskyGet(self, params)
        return doTheAPI

    def getSensorDatByAdc(self, deviceIP, adcmodule):
        mosi = "10"
        miso = "9"
        clk = "11"
        ce = "8"
        spiDat = None
        opts = [deviceIP, "spi", adcmodule, mosi, miso, clk, ce]
        sensorDat = None
        try:
	    sensorDat = sensornetwork(self, opts)
            datJson = json.loads(sensorDat)
            etLogKey = datJson.keys()[0]
            
            logObj = datJson[etLogKey]
            logKey = logObj.keys()[0]
            
            logContentObj = logObj[logKey]
            logContentKey = logContentObj.keys()[0]
            
            for i in xrange(len(logContentObj)):
                key = logContentObj.keys()[i]
                if key == "spi":
                    spiDat = logContentObj[key]
                    break
        except Exception, e:
            return None
        
        return spiDat
    
    def getSensorDatByAdcChannel(self, deviceIP, adcmodule, ch):
        mosi = "10"
        miso = "9"
        clk = "11"
        ce = "8"
        spiDat = None
        opts = [deviceIP, "spi", adcmodule, mosi, miso, clk, ce, ch]
        sensorDat = None
        try:
	    sensorDat = sensornetwork(self, opts)
            datJson = json.loads(sensorDat)
            etLogKey = datJson.keys()[0]
            
            logObj = datJson[etLogKey]
            logKey = logObj.keys()[0]
            
            logContentObj = logObj[logKey]
            logContentKey = logContentObj.keys()[0]
            
            
            for i in xrange(len(logContentObj)):
                key = logContentObj.keys()[i]
                if key == "spi":
                    spiDat = logContentObj[key]
                    break
        except Exception, e:
            return None
        
        return spiDat
    
    
    # Return the list of connecting embedded devices information. 
    def list_ed(self):
        params = createBlueskyParam(self, "ls", ["noneFix", "edconnected"])
        listEd = blueskyGet(self, params)
        listingDevices = json.loads(listEd)
        
        etLogKey = listingDevices.keys()        
        connStatusInfoListObj = listingDevices[etLogKey[0]]
        connStatusInfoKey = connStatusInfoListObj.keys()[0]
        return connStatusInfoListObj[connStatusInfoKey]
    
    # Convert to parameter of HTTP
    def createBlueskyParam(self, instruction, opts):
        if type(opts).__name__ == 'list':
            ret = "/etLog?instruction=" + instruction
            for i in xrange(len(opts)):
                ret += "&opt" + `i` + "=" + opts[i]
            return ret
        else:
            return None
            
    # Do something with Bluesky API
    def blueskyGet(self, blueskyParam):
        loggedin = login(self)
        
        try:
            conn = httplib.HTTPConnection(self.blueskyGateway)
            conn.request("GET", blueskyParam, headers={'Content-Type':'text/html'})
            r2 = conn.getresponse()
            data = r2.read()
        except httplib.BadStatusLine, e:
            data = None

        loggedout = logout(self)
        return data
        
    # login to the system as the public account.
    def login(self):
        for num in range(2):
            url = 'http://' + self.blueskyGateway + '/doLogin.ins'

        values = {'username' : self.username,
                  'password' : self.password,
                  'mode' : 'signin'}

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        signinResult = response.read()
        return signinResult

    # logout from the system from the account.
    def logout(self):
        for num in range(2):
            url = 'http://' + self.blueskyGateway + '/doLogout.ins'

        values = {'username' : self.username,
                  'mode' : 'signout'}

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        signoutResult = response.read()
        return signoutResult
