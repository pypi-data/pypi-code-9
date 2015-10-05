#! /usr/bin/env python
# Control audacious using dbus
from dbus import SessionBus, DBusException, Interface
import dbus
# dbus schema from audacious/src/dbus/aud-dbus.xml 
class AudBus:
    def __init__(self):
        self._session = SessionBus()
        self._bus = self._session.get_object("org.atheme.audacious",
                                             "/org/atheme/audacious")
        self._dproxy = Interface(self._bus, 'org.atheme.audacious')    
    # examine the player status
    def version(self): return self._dproxy.Version()
    def is_playing(self): return bool(self._dproxy.Playing())
    def is_paused(self): return bool(self._dproxy.Paused())
    def is_stopped(self): return bool(self._dproxy.Stopped())
    def player_status(self): return str(self._dproxy.Status())
    def position(self):
        pos = self._dproxy.Position()
        if pos == 4294967295:
            pos = -1
        return int(pos)
    def info(self):
        "returns bitrate, frequency, and number of channels. (rate,freq,nch)"
        return self._dproxy.Info()
    def time(self):
        return self._dproxy.Time()/1000 # convert to seconds
    def balance(self, balance):
        return self._dproxy.Balance(dbus.UInt32(balance))
    # ignore separate l and r volume levels, just take the l onoe
    def volume(self): return self._dproxy.Volume()[0]
    def songtitle(self, pos):
        return unicode(self._dproxy.SongTitle(dbus.UInt32(pos)))
    def songfilename(self, pos):
        return unicode(self._dproxy.SongFilename(dbus.UInt32(pos)))
    def pl_length(self):
        return int(self._dproxy.Length())
    def songlength(self, pos):
        return int(self._dproxy.SongLength(dbus.UInt32(pos)))
    def songframes(self, pos):
        return int(self._dproxy.SongFrames(dbus.UInt32(pos)))
    def songtuple(self, pos, element_name):
        return self._dproxy.SongTuple(dbus.UInt32(pos), element_name)
    def pl_titles(self, anchor, before=5, after=5, playlist_lock=False):
        # return playlist titles list sliced ala pl[anchor-before:anchor+after]
        if playlist_lock:
            pl_ind = -1
        else:
            pl_ind = int(self.getactiveplaylist())
        retVal = []
        start = anchor-before
        if anchor - before < 0: start = 0
        end = anchor+after
        real_end = self.pl_length()
        if end > real_end: end = real_end - 1
        for ind in range(start, end + 1):
            length = self.songlength(ind)
            lformat = "%02d:%02d" % (length / 60, length % 60)
            que_pos = -1        # not enqueued
            if self.playqueueisqueued(ind): 
                que_pos = self.queuegetqueuepos(ind)
            retVal.append((ind, pl_ind, self.songtitle(ind), que_pos, lformat))


        return retVal
    def playlist_names(self):
        # return playlist indexes and fake names (for all but the
        # active playlist [(pl_ind, pl_name)...]
        retVal = []
        active_pl_ind = self.getactiveplaylist()
        for ind in range(self.numberofplaylists()):
            if ind == active_pl_ind:
                label = self.getactiveplaylistname()
            else:
                label = "Playlist %d" % ind
            retVal.append((ind, label))
        return retVal 
    def gettuplefields(self, pos):
        return self._dproxy.GetTupleFields(dbus.UInt32(pos))
    # def is_mainwinvisible(self): return self._dproxy.MainWinVisible()
    def is_shuffle_mode(self): return bool(self._dproxy.Shuffle())
    def is_autoadvance(self): return bool(self._dproxy.AutoAdvance())
    def is_repeat_mode(self): return bool(self._dproxy.Repeat())
    def is_stopafter(self): return bool(self._dproxy.StopAfter())
    def queuegetlistpos(self, pos):
        return self._dproxy.QueueGetListPos(dbus.UInt32(pos))
    def queuegetqueuepos(self, pos):
        return self._dproxy.QueueGetQueuePos(dbus.UInt32(pos))
    def getinfo(self): return self._dproxy.GetInfo()
    def getplayqueuelength(self): return self._dproxy.GetPlayqueueLength()
    def playqueueisqueued(self, pos):
        return self._dproxy.PlayqueueIsQueued(dbus.UInt32(pos))
    # def geteq(self): return self._dproxy.GetEq()
    # def geteqpreamp(self): return self._dproxy.GetEqPreamp()
    # def geteqband(self): return self._dproxy.GetEqBand()
    def numberofplaylists(self): return int(self._dproxy.NumberOfPlaylists())
    def getactiveplaylist(self): return int(self._dproxy.GetActivePlaylist())
    def getactiveplaylistname(self): 
        return str(self._dproxy.GetActivePlaylistName())

    # control the player
    def quit(self): self._dproxy.Quit()
    # def eject(self): self._dproxy.Eject()
    # def showmainwin(self, pred): self._dproxy.ShowMainWin(pred)
    def play(self): self._dproxy.Play()
    def pause(self): self._dproxy.Pause()
    def stop(self): self._dproxy.Stop()
    def seek(self, pos):
        self._dproxy.Seek(dbus.UInt32(pos))
    def lower_volume(self, amount=10):
        current_vol = self.volume()
        new_vol = current_vol - amount
        if new_vol < 0: new_vol = 0
        self.setvolume(new_vol, new_vol)
    def raise_volume(self, amount=10):
        current_vol = self.volume()
        new_vol = current_vol + amount
        if new_vol > 100: new_vol = 100
        self.setvolume(new_vol, new_vol)
    def setvolume(self, left, right):
        self._dproxy.SetVolume(left, right)
    def advance(self): self._dproxy.Advance()
    def reverse(self): self._dproxy.Reverse()
    def jump(self, pos):
        self._dproxy.Jump(dbus.UInt32(pos))
    # def add(self, filename): self._dproxy.Add(filename)
    def addurl(self, url):
        self._dproxy.AddUrl(url)
    # def addlist(self, filename_list): self._dproxy.AddList(filename_list)
    # def openlist(self, filename_list): self._dproxy.OpenList(filename_list)
    # def openlisttotemp(self, filename_list):
    #     self._dproxy.OpenListToTemp(filename_list)
    def delete(self, pos):
        self._dproxy.Delete(dbus.UInt32(pos))
    def clear(self): return self._dproxy.Clear()
    def toggleautoadvance(self): self._dproxy.ToggleAutoAdvance()
    def togglerepeat(self): self._dproxy.ToggleRepeat()
    def toggleshuffle(self): self._dproxy.ToggleShuffle()
    def togglestopafter(self): self._dproxy.ToggleStopAfter()
    # def showprefsbox(self, pred): return self._dproxy.ShowPrefsBox(pred)
    # def showaboutbox(self, pred): return self._dproxy.ShowAboutBox(pred)
    # def showjtfbox(self, pred): return self._dproxy.ShowJtfBox(pred)
    # def showfilebrowser(self, pred): return self._dproxy.ShowFilebrowser(pred)
    def playpause(self): self._dproxy.PlayPause()
    def playlistinsurlstring(self, url, pos):
        self._dproxy.PlaylistInsUrlString(url, dbus.UInt32(pos))
    def playlistadd(self, pos):
        self._dproxy.PlaylistAdd(dbus.UInt32(pos))
    def playqueueadd(self, pos):
        self._dproxy.PlayqueueAdd(dbus.UInt32(pos))
    def playqueuetoggle(self, pos):
        if self.playqueueisqueued(pos):
            self._dproxy.PlayqueueRemove(dbus.UInt32(pos))
        else:
            self._dproxy.PlayqueueAdd(dbus.UInt32(pos))

    def playqueueremove(self, pos):
        self._dproxy.PlayqueueRemove(dbus.UInt32(pos))
    def playqueueclear(self): self._dproxy.PlayqueueClear()
    def playlistenqueuetotemp(self, url):
        self._dproxy.PlaylistEnqueueToTemp(url)
    # def seteq(self, preamp): self._dproxy.SetEq(dbus.Double(preamp))
    # def geteqpreamp(self, preamp): self._dproxy.SetEqPreamp(dbus.Double(preamp))
    # def seteqband(self, band, value):
    #     self._dproxy.SetEqBand(dbus.UInt32(band),dbus.Double(value))
    # def equalizeractivate(self, pred): self._dproxy.EqualizerActivate(pred)
    def setactiveplaylist(self, pl_pos):
        # running this without running playactiveplaylist leaves
        # this i/f inconsistent wrt what track is playing;fixed in audacious 3.7
        self._dproxy.SetActivePlaylist(pl_pos)
    def newplaylist(self): self._dproxy.NewPlaylist()
    def deleteactiveplaylist(self): self._dproxy.DeleteActivePlaylist()
    def playactiveplaylist(self): self._dproxy.PlayActivePlaylist()

if __name__ == '__main__':
    aud_handle = AudBus()
    print "version=", aud_handle.version()
    track_position = aud_handle.position()
    title = track_name = ""
    length = 0
    if track_position > -1:
        track_name = aud_handle.songtitle(track_position)
        length = aud_handle.songlength(track_position)
        title = aud_handle.songtuple(track_position, u'title')
    seconds = aud_handle.time()
    # this playlist is the selected one, not the playing one
    playlist_name = aud_handle.getactiveplaylistname() 
    print "disp=%s %02d:%02d/%02d:%02d from %s" % (track_name, 
                                                   seconds / 60, seconds % 60,
                                                   length / 60, length % 60,
                                                   playlist_name)
    if track_position > -1:
        tuple_names = [u'title', u'artist', u'album', u'codec']
        #tuple_names = aud_handle.gettuplefields(track_position)
        for n in tuple_names:
            print "%s:%s" % (n, aud_handle.songtuple(track_position, n))
    else:
        print "No track selected"
