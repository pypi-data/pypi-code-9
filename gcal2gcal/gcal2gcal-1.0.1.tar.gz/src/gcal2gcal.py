import LUADictParser,LUADictLexer
import sys
import antlr3
import codecs
import time
from datetime import datetime,timedelta,date
import os

import getpass
from optparse import OptionParser

import gdata.calendar.service
import gdata.service

import atom
import plistservices
import platform

CLASSABBREVS = {
    'L': 'Paladin',
    'D': 'Druid',
    'W': 'Warrior',
    'R': 'Rogue',
    'P': 'Priest',
    'S': 'Shaman',
    'H': 'Hunter',
    'K': 'Warlock',
    'M': 'Mage',
    'T': 'Death Knight',
    '?': 'Unknown'
}

RACEABBREVS = {
    'H': 'Human',
    'D': 'Dwarf',
    'A': 'Draenei',
    'G': 'Gnome',
    'N': 'Night Elf',
    'B': 'Blood Elf',
    'U': 'Undead',
    'R': 'Troll',
    'T': 'Tauren',
    'O': 'Orc',
    '?': 'Unknown'
}


TYPEABBREVS = {
    'Meeting':  "Event",
    'Meet': "Event",
    'Birthday':  "Birthday",
    'Birth':  "Birthday",
    'Roleplay':  "Roleplaying",
    'Holiday':  "Holiday",
    'Dentist':  "Dentist",
    'Doctor':  "Doctor",
    'Vacation':  "Vacation",
    'Other':  "Other",
    'AQR':  "Ruins of Ahn'Qiraj",
    'AQT':  "Ahn'Qiraj Temple",
    'BFD':  "Blackfathom Deeps",
    'BRD':  "Blackrock Depths",
    'UBRS':  "Blackrock Spire (Upper)",
    'LBRS':  "Blackrock Spire (Lower)",
    'BWL':  "Blackwing Lair",
    'Deadmines':  "The Deadmines",
    'DM':  "Dire Maul",
    'Gnomer':  "Gnomeregan",
    'Mara':  "Maraudon",
    'MC':  "Molten Core",
    'Onyxia':  "Onyxia's Lair",
    'RFC':  "Ragefire Chasm",
    'RFD':  "Razorfen Downs",
    'RFK':  "Razorfen Kraul",
    'SM':  "Scarlet Monastery",
    'Scholo':  "Scholomance",
    'SFK':  "Shadowfang Keep",
    'Stockades':  "The Stockades",
    'Strath':  "Stratholme",
    'ST':  "The Sunken Temple",
    'Uld':  "Uldaman",
    'WC':  "Wailing Caverns",
    'ZF':  "Zul'Farrak",
    'ZG':  "Zul'Gurub",
    'Naxx':  "Naxxramas",
    'TheEye':  "The Eye",
    'Serpentshrine':  "Serpentshrine",
    'Magtheridon':  "Magtheridon",
    'Hyjal':  "Mount Hyjal",
    'Karazhan':  "Karazhan",
    'ZulAman':  "Zul'Aman",
    'Gruul':  "Gruul's Lair",
    'BlackTemple':  "Black Temple",
    'Arcatraz':  "Tempest: Arcatraz",
    'Botanica':  "Tempest: Botanica",
    'Mechanar':  "Tempest: Mechanar",
    'Durnholde':  "CoT: Durnholde Keep",
    'DarkPortal':  "CoT: Black Morass (Dark Portal)",
    'AuchenaiCrypts':  "Auchindoun: Crypts",
    'SethekkHalls':  "Auchindoun: Sethekk Halls",
    'ShadowLabyrinth':  "Auchindoun: Labyrinth",
    'ManaTombs':  "Auchindoun: Mana Tombs",
    'Steamvault':  "Coilfang: Steamvault",
    'Underbog':  "Coilfang: Underbog",
    'SlavePens':  "Coilfang: Slave Pens",
    'ShatteredHalls':  "Hellfire: Shattered Halls",
    'Furnace':  "Hellfire: Blood Furnace",
    'Ramparts':  "Hellfire: Ramparts",
    'ArcatrazH':  "Tempest: Arcatraz (Heroic)",
    'BotanicaH':  "Tempest: Botanica (Heroic)",
    'MechanarH':  "Tempest: Mechanar (Heroic)",
    'DurnholdeH':  "CoT: Durnholde Keep (Heroic)",
    'DarkPortalH':  "CoT: Dark Portal (Heroic)",
    'AuchenaiCryptsH':  "Auchindoun: Crypts (Heroic)",
    'SethekkHallsH':  "Auchindoun: Sethekk Halls (Heroic)",
    'ShadowLabyrinthH':  "Auchindoun: Labyrinth (Heroic)",
    'ManaTombsH':  "Auchindoun: Mana Tombs (Heroic)",
    'SteamvaultH':  "Coilfang: Steamvault (Heroic)",
    'UnderbogH':  "Coilfang: Underbog (Heroic)",
    'SlavePensH':  "Coilfang: Slave Pens (Heroic)",
    'ShatteredHallsH':  "Hellfire: Shattered Halls (Heroic)",
    'FurnaceH':  "Hellfire: Blood Furnace (Heroic)",
    'RampartsH':  "Hellfire: Ramparts (Heroic)",
    'Magisters':  "Magister's Terrace",
    'MagistersH':  "Magister's Terrace (Heroic)",
    'Sunwell':  "Sunwell Plateau",
    'PvP':  "General PvP",
    'A2v2':  "Arena (2v2)",
    'A3v3':  "Arena (3v3)",
    'A5v5':  "Arena (5v5)",
    'AB':  "Arathi Basin",
    'AV':  "Alterac Valley",
    'WSG':  "Warsong Gulch",
    'EotS':  "Eye of the Storm",
    'DoomWalker':  "Doomwalker",
    'DoomLordKazzak':  "Doom Lord Kazzak",
    'Ahnkalet':  "Ahn'kahet: The Old Kingdom",
    'AzjolNerub':  "Azjol-Nerub",
    'Culling':  "CoT: The Culling of Stratholme",
    'DrakTharon':  "Drak'Tharon Keep",
    'Gundrak':  "Gun'Drak",
    'TheNexus':  "The Nexus",
    'TheOculus':  "The Oculus",
    'HallsofLightning':  "Ulduar: Halls of Lightning",
    'HallsofStone':  "Ulduar: Halls of Stone",
    'Utgarde':  "Utgarde Keep",
    'SUtgardePinnacle':  "Utgarde Pinnacle",
    'TheVioletHold':  "Violet Hold",
    'AhnkaletH':  "Ahn'kahet: The Old Kingdom (Heroic)",
    'AzjolNerubH':  "Azjol-Nerub (Heroic)",
    'CullingH':  "CoT: The Culling of Stratholme (Heroic)",
    'DrakTharonH':  "Drak'Tharon Keep (Heroic)",
    'GundrakH':  "Gun'Drak (Heroic)",
    'TheNexusH':  "The Nexus (Heroic)",
    'TheOculusH':  "The Oculus (Heroic)",
    'HallsofLightningH':  "Ulduar: Halls of Lightning (Heroic)",
    'HallsofStoneH':  "Ulduar: Halls of Stone (Heroic)",
    'UtgardeH':  "Utgarde Keep (Heroic)",
    'UtgardePinnacleH':  "Utgarde Pinnacle (Heroic)",
    'TheVioletHoldH':  "Violet Hold (Heroic)",
    'NaxxH':  "Naxxramas (Heroic)",
    'Eternity':  "The Eye of Eternity",
    'EternityH':  "The Eye of Eternity (Heroic)",
    'Obsidian':  "The Obsidian Sanctum",
    'ObsidianH':  "The Obsidian Sanctum (Heroic)",
    'Archavon':  "Vault of Archavon",
    'ArchavonH':  "Vault of Archavon (Heroic)",
    'ZGReset':  "Zul'Gurub Resets",
    'MCReset':  "Molten Core Resets",
    'OnyxiaReset':  "Onyxia Resets",
    'BWLReset':  "Blackwing Lair Resets",
    'AQRReset':  "Ruins of Ahn'Qiraj Resets",
    'AQTReset':  "Ahn'Qiraj Temple Resets",
    'NaxxReset':  "Naxxramas Resets",
    'KarazhanReset':  "Karazhan Resets",
    'ZulAmanReset':  "Zul'Aman Resets",
    'BlackTempleReset':  "Black Temple Resets",
    'TheEyeReset':  "The Eye Resets",
    'SerpentshrineReset':  "Serpentshrine Resets",
    'MagtheridonReset':  "Magtheridon Resets",
    'HyjalReset':  "Mount Hyjal Resets",
    'GruulReset':  "Gruul's Lair Resets",
    'SunwellReset':  "Sunwell Plateau Resets",
    'TransmuteCooldown':  "Transmute Available",
    'AlchemyResearchCooldown':  "Alchemy Research Available",
    'SaltShakerCooldown':  "Salt Shaker Available",
    'MoonclothCooldown':  "Mooncloth Available",
    'PrimalMoonclothCooldown':  "Primal Mooncloth Available",
    'SpellclothCooldown':  "Spellcloth Available",
    'ShadowclothCooldown':  "Shadowcloth Available",
    'EbonweaveCooldown':  "Ebonweave Available",
    'SpellweaveCooldown':  "Spellweave Available",
    'MoonshroudCooldown':  "Moonshroud Available",
    'SnowmasterCooldown':  "SnowMaster 9000 Available",
    'BrilliantGlassCooldown':  "Brilliant Glass Available",
    'VoidShatterCooldown':  "Void Shatter Available",
    'VoidSphereCooldown':  "Void Sphere Available",
    'InscriptionCooldown':  "Inscription Research Available",
    'Inscription2Cooldown':  "Northrend Inscription Research Available",
    'TitansteelCooldown':  "Smelt Titansteel Available",
}

TYPEZONES = {
    'Ahnkalet':  "Dragonblight",
    'AzjolNerub':  "Dragonblight",
    'Culling':  "Tanaris",
    'DrakTharon':  "Grizzly Hills",
    'Gundrak':  "Zul'Drak",
    'TheNexus':  "Coldara",
    'TheOculus':  "Coldara",
    'HallsofLightning':  "Storm Peaks",
    'HallsofStone':  "Storm Peaks",
    'Utgarde':  "Howling Fjord",
    'SUtgardePinnacle':  "Howling Fjord",
    'TheVioletHold':  "Dalaran",
    'AhnkaletH':  "Dragonblight",
    'AzjolNerubH':  "Dragonblight",
    'CullingH':  "Tanaris",
    'DrakTharonH':  "Grizzly Hills",
    'GundrakH':  "Zul'Drak",
    'TheNexusH':  "Coldara",
    'TheOculusH':  "Coldara",
    'HallsofLightningH':  "Storm Peaks",
    'HallsofStoneH':  "Storm Peaks",
    'UtgardeH':  "Howling Fjord",
    'UtgardePinnacleH':  "Howling Fjord",
    'TheVioletHoldH':  "Dalaran",
    'NaxxH':  "Dragonblight",
    'Eternity':  "Coldara",
    'EternityH':  "Coldara",
    'Obsidian':  "Dragonblight",
    'ObsidianH':  "Dragonblight",
    'Naxx': "Dragonblight",
    'NaxH': "Dragonblight",
    'Archavon':  "Wintergrasp",
    'ArchavonH':  "Wintergrasp",
}

class AttendeeInfo:
    def __init__(self,name,data):
        self.name = name
        data = data.split(',')
        info = data[3]
        self.race = RACEABBREVS[info[0]]
        self.clazz = CLASSABBREVS[info[1]]
        self.level = int(info[2:])

    def __str__(self):
        s = self.name + ' ' + `self.level` + ' ' + self.race + ' ' + self.clazz
        return s

    def __repr__(self):
        return self.__str__()
    
class Event:
    def __init__(self,data,c):
        self.data = data
        #convert time
        #GC gives days since Jan 1 2000 and hours since midnight
        delta = timedelta(days=int(self.data['mDate']))
        self.time = datetime(2000,1,1) + delta
        if 'mTime' in self.data:
            delta = timedelta(minutes=int(self.data['mTime']))
            self.time += delta
        if 'mDuration' in self.data:
            self.duration = timedelta(minutes=self.mDuration)
        else:
            self.duration = None
        self.creator = c
        self.type = TYPEABBREVS.get(self.mType,self.mType)
        self.title = self.type
        if self.mTitle:
            self.title += ' -- ' + fixEscapedCharacters(self.mTitle)
        if self.mAttendance:
            self.attendees = [AttendeeInfo(n,d) for n,d in self.mAttendance.iteritems()]
        else:
            self.attendees = []
            
    def __getattr__(self,key):
        return self.data.get(key,None)

    def toGoogleEvent(self):
        gevent = gdata.calendar.CalendarEventEntry()
        gevent.where.append(gdata.calendar.Where(value_string=TYPEZONES.get(self.mType, "Unknown")))
        gevent.author.append(atom.Author(name=atom.Name(text=self.creator),text=self.creator))
        gevent.source = atom.Name(text=self.creator)
        #for a in self.attendees:
        #    w = gdata.calendar.Who(text=str(a))
        #    w.name = atom.Name(text=str(a))
        #    gevent.who.append(w)
        gevent.title = atom.Title(text=self.title)
        c = ''
        if self.mDescription:
            c += fixEscapedCharacters(self.mDescription) + '\n'
        c += self.attendanceAsString()
        gevent.content = atom.Content(text=c)
        start_time = self.time.isoformat()
        if self.duration:
            end_time = (self.time + self.duration).isoformat()
        else:
            if 'mTime' in self.data:
                end_time = (self.time + timedelta(minutes=60)).isoformat()
            else:
                end_time = (self.time + timedelta(minutes=1440)).isoformat()
        gevent.when.append(gdata.calendar.When(start_time=start_time,end_time=end_time))
        gevent.extended_property.append(gdata.calendar.ExtendedProperty(name='gc_id',value=str(self.mID)))
        return gevent
    
    def attendanceAsString(self):
        s = ''
        if 'mAttendance' in self.data:
            s += `len(self.mAttendance)` + ' characters signed up:\n'
            for n,d in self.mAttendance.iteritems():
                a = AttendeeInfo(n,d)
                s += '  ' + unicode(a) + '\n'
        return s
        
    def __str__(self):
        s = str(self.time) + ': ' + str(self.type)
        if 'mDescription' in self.data:
            s += ' "' + self.mDescription + '"'
        #s += "\n" + self.attendanceAsString()
        return s

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return unicode(self.__str__())

class Preferences:
    def __init__(self):
        self.config = {}
        self.loadPrefs()

    def loadPrefs(self):
        self.config = {}
        if platform.system() == 'Darwin':
            path = os.path.join(os.path.expanduser('~'),'Library/Preferences/org.grentius.gcal2gcal.plist')
        else:
            path = os.path.join(os.path.expanduser('~'),'.org.grentius.gcal2gcal.plist')

        if os.path.exists(path):
            data = plistservices.Data.dataWithOpenFile(open(path))
            self.config = plistservices.propertyListFromData(data)

    def savePrefs(self): 
        if platform.system() == 'Darwin':
            path = os.path.join(os.path.expanduser('~'),'Library/Preferences/org.grentius.gcal2gcal.plist')
        else:
            path = os.path.join(os.path.expanduser('~'),'.org.grentius.gcal2gcal.plist')
        f = open(path,'w')
        f.write(plistservices.dataFromPropertyList(self.config).bytes())
        f.close()

    def getPref(self, key, default = None, override = None):
        if override != None:
            self.config[key] = override
            return override
        if key in self.config:
            return self.config[key]
        elif default != None:
            self.config[key] = default
            return default

    def setPref(self, key, value):
        self.config[key] = value

class WoWDir:
    def __init__(self, prefs, path=None):
        self.prefs = prefs
        self.path = self.prefs.getPref('WoWPath','/Applications/World of Warcraft/',path)

    def setPath(self, path):
        self.path = path
        if self.scanPath():
            self.prefs.setPref('WoWPath',path)
            return True
        else:
            return False
            

    def getPath(self):
        return self.path

    def scanPath(self):
        print 'scanning WoW dir at "' + self.path + '"'
        self.accountList = {}
        self.accountPath = os.path.join(self.path,'WTF','Account')
        if not (os.path.exists(self.accountPath)
                and os.path.isdir(self.accountPath)):
            return False

        for d in os.listdir(self.accountPath):
            if d.startswith('.'):
                continue
            print 'checking account',d + ':',
            fullPath = os.path.join(self.accountPath,d)
            calFile = os.path.join(fullPath,
                               'SavedVariables',
                               'GroupCalendar.lua')
            if os.path.exists(calFile):
                self.accountList[d] = calFile
                print 'has GroupCalendar data'
            else:
                print 'has no GroupCalendar data'

        if not self.accountList:
            print >>sys.stderr,'ERROR: No accounts with GroupCalendar data found.'
            return False
        print 'found accounts with GroupCalendar data:',
        for a in self.accountList.keys():
            print a + ' ',
        print
        return True

    def getAccounts(self):
        return self.accountList.keys()

    def getFilePath(self, account=None):
        if not account and len(self.accountList):
            account = self.accountList.keys()[0]
        self.prefs.getPref('WoWAccount', None, account)
        if not account in self.accountList:
            print >>sys.stderr,'ERROR: no such wow account',account,'use --account'
            sys.exit(1)
        return self.accountList[account]
        
            
class GC2GC:
    def __init__(self, prefs, calendarString=None, backDays=None, forwardDays=None):        
        self.prefs = prefs
        self.calendarID = self.prefs.getPref('TargetGoogleCalendar', None, calendarString)
        if not self.calendarID:
            print >>sys.stderr,'ERROR: need a target google calendar specified, use --calendar'
            sys.exit(1)
        backDays = self.prefs.getPref('DaysBackwards', 14, backDays)
        forwardDays = self.prefs.getPref('DaysForward', 60, forwardDays)

        self.start = datetime.now() - timedelta(days=backDays)
        self.end = datetime.now() + timedelta(days=forwardDays)
        self.inserted = 0
        self.updated = 0

    def login(self, passw, email=None):
        login = self.prefs.getPref('GoogleLogin', None, email)
        if not login:
            print >>sys.stderr,'ERROR: need valid google login id, use --user'
            sys.exit(1)
        self.client = gdata.calendar.service.CalendarService()
        self.client.email = login
        self.client.password = passw
        self.client.source = 'gc2gc-0.1'
        self.client.ProgrammaticLogin()
        return self.client

    def deleteEvents(self):
        query = gdata.calendar.service.CalendarEventQuery(self.calendarID,'private','full')
        query.start_min = self.start.isoformat()
        query.start_max = self.end.isoformat()
        feed = self.client.CalendarQuery(query)

        count = 0
        for event in feed.entry:
            self.client.DeleteEvent(event.GetEditLink().href)
            count += 1
        print 'deleted',count,'events between',self.start,'and',self.end
        
    def maybeInsertEvent(self, event):
        #see if event already exists
        query = gdata.calendar.service.CalendarEventQuery(self.calendarID,'private','full')
        query.start_min = event.time.isoformat()
        query.start_max = (event.time + timedelta(days=1)).isoformat()
        feed = self.client.CalendarQuery(query)

        gevent = event.toGoogleEvent()
        
        foundEvent = False
        for e in feed.entry:
            #print e.title.text,event.title
            #print e
            for p in e.extended_property:
                if p.name == 'gc_id' and int(p.value) == event.mID:
                    self.client.UpdateEvent(e.GetEditLink().href,gevent)
                    self.updated += 1
                    print 'updated'
                    foundEvent = True
                    break
            if foundEvent:
                break
        else:
            self.inserted += 1
            print 'inserted'
            new_event = self.client.InsertEvent(gevent,
                                                '/calendar/feeds/' + self.calendarID + '/private/full',
                                                escape_params=True)
        #print 'inserting',event
    
    @staticmethod
    def doParse(fname):
        s = antlr3.StringStream(codecs.open(fname,'r','utf-8').read())
        l = LUADictLexer.LUADictLexer(s)
        t = antlr3.CommonTokenStream(l)
        p = LUADictParser.LUADictParser(t)
        r = p.savedVars()
        return r['gGroupCalendar_Database']

    @staticmethod
    def makeEvents(db):
        l = []
        for data in db.values():
            toon = data['UserName']
            events = data['Events']
            for eventlist in events.values():
                for event in eventlist.values():
                    l.append(Event(event,toon))
        return l
            
    def parseLUA(self, fname=None):
        self.inserted = 0
        self.updated = 0
        self.db = GC2GC.doParse(fname)
        if self.db['Format'] < 14 or self.db['Format'] > 19:
            print >>sys.stderr,'WARNING: only verified for GC db format version 14-19, actual format is',self.db['Format']
        self.db = self.db['Databases']

    def upload(self):
        events = GC2GC.makeEvents(self.db)
        for e in events:
            if not e.mPrivate and e.time > self.start and e.time < self.end:
                print 'handling',unicode(e).encode('latin_1'),e.mID,
                self.maybeInsertEvent(e)
        print 'updated',self.updated,'inserted',self.inserted,'events'
           
def fixEscapedCharacters(escapedString):
    escapedString = escapedString.replace('&s;', '/')
    escapedString = escapedString.replace('&c;', ',')
    escapedString = escapedString.replace('&cn;', ':')
    return escapedString
 
def readoptions():
    parser = OptionParser()
    parser.add_option('-u', '--user', type="string", dest="login", help="Google calendar login name")
    parser.add_option('-d','--wowdir', type="string", dest="wowdir", help="WoW Application Directory")
    parser.add_option('-b','--back', type="int", dest="daysBack", help="Number of Days before current date to upload")
    parser.add_option('-f','--forward', type="int", dest="daysForward", help="Number of Days after current date to upload")
    parser.add_option('-a','--account', type="string", dest="account", help="WoW account name to use")
    parser.add_option('-c','--calendar', type="string", dest="gcal", help="private id of google calendar to use (get from google cal - of the form XXXgroup.calendar.google.com where XXX is a gibberish string.)")
    parser.add_option('-p','--prefs',action="store_true", dest="list_prefs", help="print saved preferences")
    parser.add_option('--file', type="string", dest="file", help="use specific file instead of account's GroupCalendar.lua")

    (options,args) = parser.parse_args()

    prefs = Preferences()

    return (options,prefs)

def main():
    (options,prefs) = readoptions()

    if options.list_prefs:
        import pprint
        pprint.pprint(prefs.config)
        sys.exit(0)

    try:
        #specifying a file overrides all acount info, mainly for debugging
        if options.file:
            db = GC2GC.doParse(options.file)
            events = GC2GC.makeEvents(db['Databases'])
            print [unicode(e).encode('utf-8') for e in events]
            sys.exit(0)
        wow = WoWDir(prefs, options.wowdir)
        if not wow.scanPath():
            print >>sys.stderr,'ERROR: invalid WoW Dir',wow.accountPath,'specify with --wowdir'
            sys.exit(1)
        prefs.savePrefs()
        g = GC2GC(prefs, options.gcal, options.daysBack, options.daysForward)
        prefs.savePrefs()
        g.login(passw=getpass.getpass(), email=options.login)
        prefs.savePrefs()
        g.parseLUA(wow.getFilePath(options.account))
        prefs.savePrefs()
        g.upload()
        prefs.savePrefs()
    except gdata.service.RequestError, args:
        print
        print >>sys.stderr,'ERROR: An error occured accessing your google calendar: ',
        print args
        print 'ERROR: Please make sure that',prefs.getPref('TargetGoogleCalendar', None, options.gcal),'is a valid URL and specifies your target calendar correctly - see the gcal2gcal wiki for how to do so'
        sys.exit(1)
    except gdata.service.BadAuthentication, args:
        print 'ERROR logging in to Google Calendar:',args
        print
    except SystemExit:
        #this is fine, we're already exiting and may have printed error message
        pass
    except KeyboardInterrupt:
        pass
    except:
        print
        print >>sys.stderr,'ERROR: An unhandled error occured, please report at http://code.google.com/p/gcal2gcal/issues/list with the following trace'
        print
        raise

if __name__ == '__main__':
    main()
