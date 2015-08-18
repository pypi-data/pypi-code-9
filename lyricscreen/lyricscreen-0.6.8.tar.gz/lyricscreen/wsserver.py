"""

Daniel "lytedev" Flanagan
http://dmf.me

Simple websocket server implementation.

"""

import lyricscreen, sys, asyncio, websockets, pprint, signal, jsonpickle

from .playlist import Playlist
from .song import Song
from .utils import directory_entries
from .settings import settings

class WebSocketServer(object):
    def __init__(self, loop = None):
        """Initialization for a Playlist-managing websocket server"""
        # Hosting information
        self.host = settings.websocket_host
        self.port = settings.websocket_port

        # Sockets to keep track of
        self.displays = []
        self.consoles = []

        # Set our async event loop
        self.loop = loop

        # Build our message/handler map
        self.message_map = {
            # A message requesting the current Playlist state
            "state": self.sendState,

            # Go to the next Verse
            "next verse": self.nextVerse,

            # Go to the previous Verse
            "previous verse": self.previousVerse,
            "prev verse": self.previousVerse,

            # Go to the next Song
            "next song": self.nextSong,

            # Go the the previous Song
            "previous song": self.previousSong,
            "prev song": self.previousSong,

            # Toggle `isBlank` flag
            "toggle blank": self.toggleBlank,

            # Toggle `isFrozen` flag
            "toggle freeze": self.toggleFrozen,
            "toggle frozen": self.toggleFrozen,

            # Move to start of Playlist
            "restart playlist": self.restartPlaylist,

            # Move to end of Playlist
            "finish playlist": self.finishPlaylist,

            # Hot reload Playlist
            "reload playlist": self.reloadPlaylist,

            # Load a Playlist
            "load playlist": self.loadPlaylist,

            # Go to a Verse
            "goto verse": self.gotoVerse,

            # Switch to the specified Song Map
            "goto map": self.gotoMap,

            # Go to a Song
            "goto song": self.gotoSong,

            # Kill the server
            "kill": self.killServer,

            # List available Playlists
            "list playlist": self.listPlaylists,
            "list playlists": self.listPlaylists,

            # List available Songs
            "list song": self.listSongs,
            "list songs": self.listSongs,

            # New Playlist
            "new playlist": self.newPlaylist,

            # New Song
            "new song": self.newSong,

            # Add Song to Playlist
            "add song": self.addSong,

            # Acknowledge/Pong
            "syn": self.ackClient,
            "ping": self.pongClient,
        }

        # Load default playlist

        playlist_name = None
        if "default_playlist" in settings:
            playlist_name = settings.default_playlist

        if playlist_name == None:
            self.loadPlaylist()
        else:
            self.loadPlaylist(playlist_name)

    def sendState(self, sock, msg):
        """Message Handler: Send the current Playlist state to the given socket"""
        self.output("Sending state...")
        yield from sock.send("state: " + jsonpickle.encode(self.playlist))

    def nextVerse(self, sock, msg):
        """Message Handler: Move our Playlist to the next verse"""
        check = self.checkVerse()
        if check[0] == True:
            self.playlist.nextVerse()
        yield from self.updateAll()

    def previousVerse(self, sock, msg):
        """Message Handler: Move our Playlist to the previous Verse"""
        check = self.checkVerse()
        if check[0] == True:
            self.playlist.previousVerse()
        yield from self.updateAll()

    def nextSong(self, sock, msg):
        """Message Handler: Move our Playlist to the next Song"""
        check = self.checkSong()
        if check[0] == True:
            self.playlist.nextSong().restart()
        yield from self.updateAll()

    def previousSong(self, sock, msg):
        """Message Handler: Move our Playlist to the previous Song"""
        check = self.checkSong()
        if check[0] == True:
            self.playlist.previousSong().restart()
        yield from self.updateAll()

    def toggleBlank(self, sock, msg):
        """Message Handler: Toggle the Playlist's `isBlank` flag"""
        if self.playlist:
            self.playlist.isBlank = not self.playlist.isBlank
        yield from self.updateAll()

    def toggleFrozen(self, sock, msg):
        """Message Handler: Toggle the Playlist's `isFrozen` flag"""
        if self.playlist:
            self.playlist.isFrozen = not self.playlist.isFrozen
        yield from self.updateAll()

    def restartPlaylist(self, sock, msg):
        """Message Handler: Jump to the very beginning of the Playlist."""
        if self.checkPlaylist()[0]:
            self.playlist.restart()
        yield from self.updateAll()

    def finishPlaylist(self, sock, msg):
        """Message Handler: Jump to the very beginning of the Playlist."""
        if self.checkPlaylist()[0]:
            self.playlist.finish()
        yield from self.updateAll()

    def reloadPlaylist(self, sock, msg):
        """Message Handler: Reload the current Playlist but try to remember our current
        Song, Map, Verse, etc."""
        yield from self.output("Reloading Playlist...")
        if self.checkAll()[0]:
            curSong = self.playlist.currentSong
            curMap = self.playlist.getCurrentSong().currentMap
            curVerse = self.playlist.getCurrentSong().getCurrentMap().currentVerse
            isBlank = self.playlist.isBlank
            isFrozen = self.playlist.isFrozen
        self.loadPlaylist(self.playlist.file)
        if self.checkAll()[0]:
            self.playlist.isBlank = isBlank
            self.playlist.isFrozen = isFrozen
            s = self.playlist.goToSong(curSong)
            if self.checkSong()[0]:
                m = s.goToMap(curMap)
                if self.checkVerse()[0]:
                    m.goToVerse(curVerse)
        yield from self.updateAll()

    def loadPlaylist(self, sock, msg):
        """Message Handler: Load the specified Playlist."""
        self.loadPlaylist(msg)
        yield from self.updateDisplays()

    def gotoVerse(self, sock, msg):
        """Message Handler: Jump to the specified Verse in the current Song."""
        try:
            vid = int(msg)
        except ValueError:
            return
        self.playlist.goToVerse(vid)
        yield from self.updateAll()

    def gotoMap(self, sock, msg):
        pass

    def gotoSong(self, sock, msg):
        """Message Handler: Jump to the specified Song in the current Playlist."""
        try:
            sid = int(msg)
        except ValueError:
            return
        self.playlist.goToSong(sid)
        yield from self.updateAll()

    def killServer(self, sock, msg):
        """Message Handler: Force the server to stop excecution."""
        sys.exit(0)

    def listPlaylists(self, sock, msg):
        """Message Handler: Provide the client with a full list of existing Playlists."""
        playlists = directory_entries(Playlist.default_dir, ".", ".txt")
        yield from sock.send("playlists: " + jsonpickle.encode(playlists))

    def listSongs(self, sock, msg):
        """Message Handler: Provide the client with a full list of existing Songs."""
        songs = directory_entries(Song.default_dir, ".", ".txt")
        yield from sock.send("songs: " + jsonpickle.encode(songs))

    def newPlaylist(self, sock, msg):
        """Message Handler: Start a new empty Playlist."""
        pass

    def newSong(self, sock, msg):
        """Message Handler: Start a new empty Song."""
        pass

    def addSong(self, sock, msg):
        """Message Handler: Add the Song with the given name to the current Playlist."""
        pass

    def ackClient(self, sock, msg):
        """Message Handler: Acknowledge the client."""
        yield from sock.send("ack")

    def pongClient(self, sock, msg):
        """Message Handler: Acknowledge the client."""
        yield from sock.send("pong")

    def loadPlaylist(self, p = "Default"):
        """Load the given Playlist."""
        if p.endswith(".txt"):
            p = p[:-4]

        self.playlist = Playlist.load(p)

        if self.playlist == False and p == "Default":
            # TODO: Create default Playlist
            self.playlist = Playlist.load(p)

        if self.playlist == False:
            if settings.verbose:
                print("Error: Could not load {0} playlist".format(p))
            return False

        # Print a quick summary of the playlist
        if len(self.playlist.songsToLoad) != len(self.playlist.songs):
            print("Loaded Playlist \"{0}\" with errors ({1} Song(s) - {2} Song(s) failed to load)".format(self.playlist.name, len(self.playlist.songs), len(self.playlist.songsToLoad) - len(self.playlist.songs)))
        else:
            print("Loaded Playlist {0} ({1} Song(s))".format(self.playlist.name, len(self.playlist.songs)))
        i = 1
        for s in self.playlist.songs:
            m = s.getCurrentMap()
            print("  {0}. {1} ({2} Verse(s) in {3} Map, {4} Map(s))".format(i, s.title, len(m.verses), m.name, len(s.maps)))
            i += 1

        self.updateAll()

    def start(self):
        """Start the server listening and connection-accepting loop."""
        if settings.verbose:
            print("Server Starting...")
        self.sock = websockets.serve(self.connection, self.host, self.port)

        our_loop = False
        if self.loop == None:
            our_loop = True
            self.loop = asyncio.get_event_loop()

        self.check_for_kill_signals()

        if our_loop:
            self.loop.run_until_complete(self.sock)

        if settings.verbose:
            print("Ready for connections at {0}:{1}".format(self.host, self.port))

        if our_loop:
            self.loop.run_forever()

    def check_for_kill_signals(self):
        self.loop.call_later(1, self.check_for_kill_signals)

    @asyncio.coroutine
    def stop(self, message = ""):
        if message.strip() != "":
            message = " - " + message
        if settings.verbose:
            print("Stopping WebSocketServer{0}".format(message))
        self.loop.close()

    @asyncio.coroutine
    def connection(self, sock, path):
        """Handle a socket connection."""
        # Identify ourselves (not required, just nice, I guess?)
        yield from sock.send("LyricScreen server " + lyricscreen.__version__)

        # Handle our connection paths
        if path.startswith("/display"):
            yield from self.displayConnection(sock, path)

        if path.startswith("/console"):
            yield from self.consoleConnection(sock, path)

    def sendToConsoles(self, message):
        """Send the given string to all Console sockets."""
        bad_consoles = []
        for sock in self.consoles:
            if not sock.open:
                bad_consoles.append(sock)
                continue
            yield from sock.send(message)
        for d in bad_consoles:
            self.consoles.remove(d)

    def sendToDisplays(self, message):
        """Send the given string to all Display sockets."""
        bad_displays = []
        for sock in self.displays:
            if not sock.open:
                bad_displays.append(sock)
                continue
            yield from sock.send(message)
        for d in bad_displays:
            self.displays.remove(d)

    def sendToAll(self, message):
        """Send string all sockets."""
        yield from self.sendToConsoles(message)
        yield from self.sendToDisplays(message)

    def output(self, s):
        """Print the string to the console and send the message to all
        sockets."""
        if settings.verbose:
            print(s)
        yield from self.sendToAll("console: {0}".format(s))

    def displayConnection(self, sock, path):
        """Handle a display connection and initialize the socket loop."""
        self.displays.append(sock)
        yield from self.output("Display connected.")

        check = self.checkAll()
        if check[0] == False:
            self.output("No playlist loaded.")
        else:
            # Update out displays (including this one)
            yield from self.updateDisplays()

        # Enter message loop and handle messages
        while True:
            # Displays don't get to do very much
            msg = yield from sock.recv()
            if msg is None or msg == "disconnect":
                break

        # Close the connection and remove the display
        self.displays.remove(sock)
        yield from self.output("Display disconnected.")

    def consoleConnection(self, sock, path):
        """Handle a console connection and initialize the socket loop."""
        self.consoles.append(sock)
        yield from self.output("Console connected.")

        if self.playlist == False:
            self.output("No playlist loaded.")
        else:
            # And the current slide
            v = self.playlist.getCurrentVerse()
            if v != False:
                yield from sock.send("slide: " + v.content)

        # Enter message loop and handle messages
        while True:
            msg = yield from sock.recv()
            if msg is not None:
                msg = msg.strip()
            if msg is None or msg == "disconnect":
                break
            else:
                handled = False
                for keyphrase in self.message_map:
                    if msg.startswith(keyphrase):
                        args = msg.replace(keyphrase, "", 1).strip()
                        callback = self.message_map[keyphrase]
                        yield from callback(sock, args)
                        handled = True
                        break
                if not handled:
                    print("Received unknown command: {0}".format(msg))

        self.consoles.remove(sock)
        yield from self.output("Console disconnected.")

    # Update Group Functions
    # Send the needed data to the appropriate sockets

    def updateDisplays(self, v = False):
        """Tell every display what to display."""
        if self.playlist.isBlank:
            # If the Playlist is blank, tell the slides to display nothing.
            yield from self.sendToDisplays("slide: " + " ")
        if v == False: # No verse specified...
            check = self.checkPlaylist()
            if check[0] == False:
                # No current valid Playlist
                yield from self.sendToDisplays("slide: " + " ")
                return
            v = self.playlist.getCurrentVerse()
        if v != False: # Given a proper verse (or we loaded the current one)
            displayState = "slide: " + v.content
            if self.playlist.isFrozen or self.playlist.isBlank:
                # Frozen or blank, we don't tell the displays to change
                yield from self.sendToConsoles(displayState)
            else:
                # Tell every socket what verse we're showing
                yield from self.sendToAll(displayState)
        else:
            # We got crazy errors up in this thang
            yield from self.output("Could not switch to specified verse (not found?)")

    def updateConsoles(self):
        """Send the entire Playlist state to the consoles."""
        state = jsonpickle.encode(self.playlist)
        for sock in self.consoles:
            yield from sock.send("state: " + state)

    def updateAll(self):
        yield from self.updateDisplays()
        yield from self.updateConsoles()

    # Checking Functions
    # Verify that we have certain bits of data for sanity reasons

    def checkAll(self):
        """Verifies we have a valid Playlist with a current valid Song and
        a current valid Verse. Returns the Playlist as data if all's well."""
        if self.playlist == False:
            return False, "no playlist", "No Playlist loaded."
        elif self.playlist.getCurrentSong() == False:
            return False, "no song in playlist", "No Songs in Playlist."
        elif self.playlist.getCurrentVerse() == False:
            return False, "no verse in song", "No Verses in Song."
        else:
            return True, self.playlist, "Check passed."

    def checkVerse(self):
        """Verifies we have a valid Playlist with a current valid Song and
        a current valid Verse. Returns the Verse as data if all's well."""
        if self.playlist == False:
            return False, "no playlist", "No Playlist loaded."
        elif self.playlist.getCurrentSong() == False:
            return False, "no song in playlist", "No Songs in Playlist."

        verse = self.playlist.getCurrentVerse()

        if verse == False:
            return False, "no verse in song", "No Verses in Song."
        else:
            return True, verse, "Check passed."

    def checkSong(self):
        """Verifies we have a valid Playlist with a current valid Song.
        Returns the Song as data if all's well."""
        if self.playlist == False:
            return False, "no playlist", "No Playlist loaded."

        song = self.playlist.getCurrentSong()

        if song == False:
            return False, "no song in playlist", "No Songs in Playlist."
        else:
            return True, song, "Check passed."

    def checkPlaylist(self):
        """Verifies we have a valid Playlist. Returns the Playlist as data if
        all's well."""
        if self.playlist == False:
            return False, "no playlist", "No Playlist loaded."
        else:
            return True, self.playlist, "Check passed."

