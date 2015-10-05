#! /usr/bin/env python
# audws: web service to control local audacious music player
#    Copyright (C) 2015  Edward F. McCurdy <efmccurdy@rogers.com>
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.

import socket, sys, os, time, getopt, re, traceback, threading, signal
from pkg_resources import resource_filename
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
from wsgiref import simple_server
from cgi import parse_qs, escape
from mako.template import Template
import aud_dbus

def guess_listening_addr():
    "Guess what address is used when listening with host= ''"
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # connecting to a UDP address doesn't send packets
    try:
        s.connect(('8.8.8.8', 0))   # N.B. needs to be on the internet
    except Exception, err:
        print(traceback.format_exc())
        s = None
    if s is not None:
        ip = s.getsockname()[0]
    else:
        addrs = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                 if not ip.startswith("127.")][:1]
        if len(addrs) > 0:
            ip = addrs[0]
        else:                  # perhaps not useful, but better than nothing
            ip = socket.gethostname()
    return ip

def codec_shortname(longname):  # space saving codec names
    if longname.startswith("MPEG-1 layer 3"):
        return "MP3"
    elif longname.startswith("Free Lossless Audio Codec"):
        return "FLAC"
    elif longname.startswith("Microsoft WAV"):
        return "WAV"
    elif longname.startswith("MPEG-2"):
        return "MP2"
    else:                       # hopefully this will be meaningfull
        return ''.join(re.findall('[A-Z]{3,5}', longname))
def chn_form_shortname(nch):    # human readable channel layouts
    if nch > 2 or nch < 1: return "%d.1" % nch # 5 channels => 5.1
    return ["mono", "stereo"][nch - 1]

class LogErrorHandler(simple_server.WSGIRequestHandler):
    # to restrict logging to errors only
    def log_request(self, *args): pass

class AudmanagerServer(WSGIServer):
    kill_thread = None    
    default_pl_mode = "play"
    playlists_locked = False
    DEFAULT_VOL_DELTA=8
    DEFAULT_TRACKLIST_LEN = 6
    def __init__(self, address, app, handler_class=WSGIRequestHandler):
        WSGIServer.__init__(self, address, handler_class)
        self.set_app(app)
        self.allow_reuse_address = True
        AudmanagerServer.kill_thread = threading.Thread(target=self.shutdown)
    @staticmethod
    def clean_exit(unused_signo=None, unused_frame=None):
        if not AudmanagerServer.kill_thread.isAlive():
            AudmanagerServer.kill_thread.start()
        AudmanagerServer.kill_thread.join()
        print " Caught interrupt, exiting"
        sys.exit(0)
    
    tr_list = Template(output_encoding="utf-8", text="""<!DOCTYPE html>
<html>
  <head>
      <meta charset="utf-8">
      <meta http-equiv="refresh" content="10"> 
      <meta name="viewport" 
          content="width=device-width, initial-scale=1.0, user-scalable=yes">
      <title>${current_title if current_title else 'AudPage'}</title>
      <style>
        body {background-color:#dcdad5;}
        table.track-list {border: 1px solid black; width:100%;}
        b.f8 {display:inline-block; width:5em; float: left;}
        .nowrap {
            white-space: nowrap;
        }
        td.current-track-name {background-color:#acbac6;}
        span.rightfloat {float: right;}
        button.pl_enq0 {width: 100%; text-align: left;background-color:hsl(208, 19%, 70%)}
        button.pl_enq1 {width: 100%; text-align: left;background-color:hsl(208, 19%, 75%)}
        button.pl_enq2 {width: 100%; text-align: left;background-color:hsl(208, 19%, 80%)}
        button.pl_enq3 {width: 100%; text-align: left;background-color:hsl(208, 19%, 85%)}
        button.pl_enq4 {width: 100%; text-align: left;background-color:hsl(208, 19%, 90%)}
        button.pl_enq5 {width: 100%; text-align: left;background-color:hsl(208, 19%, 95%)}
        meter {width: 14em;}
        button.pl_ctl {height: 4em;}
        button.pl_ctl_grey {height: 4em;opacity: 0.5;}
        button.up {
            border-top: solid 2px #eaeaea;
            border-left: solid 2px #eaeaea;
            border-bottom: solid 2px #777;
            border-right: solid 2px #777;
        }
        button.down {
            background: #bbb;
            border-top: solid 2px #777;
            border-left: solid 2px #777;;
            border-bottom:solid 2px #eaeaea;
            border-right: solid 2px #eaeaea;
        }
        button.plplay {width: 100%; text-align: left;}
        select.pl_select {font-size: 110%; font-weight: normal;}       
        /* slider; larger thumb */
        input[type=range]{
            -webkit-appearance: none;
        }
        input[type=range]::-webkit-slider-thumb {
          -webkit-appearance: none;
          border: 1px solid #000000;
          height: 1.6em;
          width: 2em;
          border-radius: 3px;
          background: #dcdad5;
          cursor: pointer;
          box-shadow: 1px 1px 1px #000000, 0px 0px 1px #0d0d0d; /* Add cool effects to your sliders! */
        }

        input[type=range]::-webkit-slider-runnable-track {
            width: 6em;
            height: 1.6em;
            background: #dcdad5;
            background-color: grey;
            border: none;
            border-radius: 3px;
        }

        input[type=range]:focus {
            outline: none;
        }

        /* All the same stuff for Firefox */
        input[type=range]::-moz-range-thumb {
          box-shadow: 1px 1px 1px #000000, 0px 0px 1px #0d0d0d;
          border: 1px solid #000000;
          height: 1.6em;
          width: 2em;
          background: #dcdad5;
          border-radius: 3px;
          cursor: pointer;
        }
      </style>
      <script>
        function zfill(num, len) {
          return (Array(len).join("0")+num).slice(-len);}
        function min_sec_pos(secs) {return zfill(Math.floor(secs/60),2) + ":" 
           + zfill(secs%60,2) + "/" + zfill(Math.floor(${track_length} / 60),2) 
           +  ":" + zfill(${track_length} % 60,2);}
      </script>
  </head>
<body>
<h3>Audacious Control Page on ${hostname}</h3>
<form name="aud_control" method="post" action="">
<div class="control_panel">
<button class="pl_ctl" name="control" type="submit" value="playpause"
     title="Toggle Pause/Playback">
  <img src="${state_play_pause}" id="Prev"/>
</button>
<button class="pl_ctl" name="control" type="submit" value="pl_prev"
    title="Prev">
  <img src="ic_skip_previous_black_48dp.png" id="Prev"/>
</button>
<button class="pl_ctl" name="control" type="submit" value="pl_next"
     title="Next">
  <img src="ic_skip_next_black_48dp.png" id="Next"/>
</button>
<button name="control" type="submit" 
  id="pl_toggle_repeat" value="pl_repeat" 
     % if is_repeat:
       class="down" title="Stop Repeat">
     % else:
       class="up" title="Start Repeat">
     % endif
  <img src="ic_repeat_black_48dp.png" id="repeat"/>
</button>
<button name="control" type="submit" 
  id="pl_toggle_shuffle" value="pl_shuffle" 
     % if is_shuffle:
       class="down" title="Stop Shuffle Advance">
     % else:
       class="up" title="Start Shuffle Advance">
     % endif
  <img src="ic_shuffle_black_48dp.png" id="shuffle"/>
</button>
<span name="vol" class="nowrap">
<button name="control" type="submit" value="volume_down"
     % if volume == 0:
       class="pl_ctl_grey"
       disabled="disabled"
     % else:
       class="pl_ctl"
     % endif
     title="Decrease volume">
 <img class="icon" src="ic_volume_down_black_48dp.png"/>
</button>
<button name="control" type="submit" value="volume_up"
     % if volume == 100:
       class="pl_ctl_grey"
       disabled="disabled"
     % else:
       class="pl_ctl"
     % endif
     title="Increase volume">
  <img class="icon" src="ic_volume_up_black_48dp.png"/>
</button>
</span>
</div>
</form>
<div>
<b>Current Track: </b>${current_title}
<br>
<form name="seek-bar" method="post" action="">
<table>
<tr><td>
<b class="f8">${state}: </b>
</td><td>
<input type="range" class="seek-bar" name="seek_control" min="0"
  max="${track_length}" onchange="this.form.submit();" id="seek-bar" 
  value="${track_pos}" oninput="document.getElementById('seek_pos').innerHTML=min_sec_pos(this.value)" title="Adjust playback position"/> 
</td> <td>
<span id="seek_pos">${current_track_pos}</span> ${audio_info}
</td></tr>
</table>
</form>
</div>
<form name="control_track" id="playlist" method="post" action=""></form>
<table class="track-list">
<tr>
% if not playlists_lock:
<td><form name="control_pl" method="post" action="">
<span name="pl_jump_control" class="nowrap">
<label for="pl_select"><b>Playlist:</b></label>
<select class="pl_select" id="pl_select" name="pl_control" type="submit"
  onchange="this.form.submit();" title="Select playlist">
  % for ind, pl_name in play_lists:
     <option value="${ind}"
     % if ind == active_pl_ind:
       selected="selected"
     % endif
     >${pl_name}</option>
  % endfor
</select>
</spen>
</form>
</td>
% endif
<td>
<form name="manage_tracklist" method="get" action="">
<span name="pl_jump_control" class="nowrap">
<label for="pl_jump_mode"><b>Click to:</b></label>
<select name="pl_jump_mode" class="pl_select" type="submit" 
  onchange="this.form.submit();">
  <option value="play"
     % if pl_mode == "play":
       selected="selected"
     % endif
  >play</option>
  <option value="enque"
     % if pl_mode == "enque":
       selected="selected"
     % endif
  >enque</option>
</select>
</span>
<input type="hidden" name="size" value="${tl_size}" />
<button class="tr-ctrl" name="size_up" id="size_more" type="submit"
  onclick="this.form.size.value = this.value"
         value="${tl_size * 2}" 
         title="Display a longer tracklist">
  <img class="sm-icon" src="ic_unfold_more_black_24dp.png"/>
</button>
<button class="tr-ctrl" name="size_down" id="size_less" type="submit"
  onclick="this.form.size.value = this.value"
         value="${tl_size / 2}" 
         title="Display a shorter tracklist">
  <img class="sm-icon" src="ic_unfold_less_black_24dp.png"/>
</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<span name="scroll" class="nowrap">
<input type="hidden" name="offset" value="${tl_offset}" />
<button class="tr-ctrl" name="offset_up" id="scroll_up" type="submit"
  onclick="this.form.offset.value = this.value"
         value="${tl_offset - 1}" 
         title="Scroll tracklist Up">
  <img class="sm-icon" src="ic_arrow_drop_up_black_24dp.png"/>
</button>
<button class="tr-ctrl" name="offset_reset" id="scroll_down" type="submit"
  onclick="this.form.offset.value = 0"
         value="0" 
         title="Reset tracklist Scrolling">
  <img class="sm-icon" src="ic_vertical_align_center_black_24dp.png"/>
</button>
<button class="tr-ctrl" name="offset_down" id="scroll_down" type="submit"
  onclick="this.form.offset.value = this.value"
         value="${tl_offset + 1}" 
         title="Scroll tracklist down">
  <img class="sm-icon" src="ic_arrow_drop_down_black_24dp.png"/>
</button>
</span>
</form>
</tr>
  % for ind, pl_ind, track, que_pos, len in tracks:
  <tr>
    <td colspan="2"
     ## distinguish current track
     % if ind == track_ind and pl_ind == active_pl_ind:
        class="current-track-name">
          ${track}&nbsp;<span class="rightfloat">
          ${len if len != '00:00' else ''}</span>
     % else:
        class="track-name">
     ## color code position in the enque list
     <%
          pl_class = "plplay"
          if que_pos >= 0:
              pl_class = "pl_enq%d" % que_pos
     %>
        <button class="${pl_class}" name="jump_control" type="submit"
          value="${ind}" form="playlist"
          title="${pl_mode.capitalize()} this track">
            ${track}&nbsp;<span class="rightfloat">
            ${len if len != '00:00' else ''}</span>
        </button>
     % endif
    </td>
  </tr>
  % endfor
</table>
</body>
</html>
""")

def application(environ, start_response): # the wsgi application
    "Web server page of controls for the audacious-media-player.org player."
    path    = environ['PATH_INFO']
    method  = environ['REQUEST_METHOD']
    query = environ['QUERY_STRING']
    form_data = parse_qs(query)
    pl_mode = form_data.get('pl_jump_mode',
                            [AudmanagerServer.default_pl_mode])[0]
    redir_url = path + "?" + query if len(query) else path
    try:
        aud_handle = aud_dbus.AudBus()
    except Exception, err:
        if type(err) == aud_dbus.DBusException:
            name = err.get_dbus_name()
            if name.startswith("org.freedesktop.DBus.Error.NoReply"):
                # a python-dbus leak eventually hangs dbus calls, so restart
                print "Audman: Fatal Exception %s at %s " \
                    % (err, time.asctime())
                print(traceback.format_exc())
                start_response('302 Found', [('Location', redir_url)])
                if not AudmanagerServer.kill_thread.isAlive():
                    AudmanagerServer.kill_thread.start()
                return ['']         # redir to retry
        status = '504 Gateway Timeout'
        response_headers = [('Content-Type', 'text/html;charset=utf8')]
        start_response(status, response_headers)
        return ["Server Error: Could not find audacious process"
                + " on the dbus:\n %s" % err]
    # process any actions, and redir back to this page (preserving query_string)
    if method == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
        except (TypeError, ValueError):
            print(traceback.format_exc())
            request_body = "0"
        try:
            response_body = str(request_body)
        except:
            response_body = "error"

        d = parse_qs(request_body)
        if not (d.has_key('control') or d.has_key('seek_control') 
                or d.has_key('jump_control')or  d.has_key('pl_control')) :
            start_response('500 INTERNAL SERVER ERROR', [
                               ('Content-Type', 'text/plain')])
            return ["Internal error: no control element in POST"]
        action = None
        if d.has_key('seek_control'):   # skip forward/backward in current track
            action = 'seek_control'
            aud_handle.seek(int(d[action][0]) * 1000)
        elif d.has_key('jump_control'): # switch to or enque a specific track
            action = 'jump_control'
            ind = int(d[action][0])
            if pl_mode == "play":
                aud_handle.jump(ind)
            else:
                aud_handle.playqueuetoggle(ind)
        elif d.has_key('pl_control'):   # switch to a different playlist
            action = 'pl_control'
            pl_ind = int(d[action][0])
            aud_handle.setactiveplaylist(pl_ind)
            aud_handle.playactiveplaylist()
        else:
            action = d["control"][0]
            if 'playpause'== action:
                aud_handle.playpause()
            elif 'stop'== action:
                aud_handle.stop()
            elif 'pl_next'== action:       # switch to the next track
                aud_handle.advance()
            elif 'pl_prev'== action:
                aud_handle.reverse()
            elif 'pl_shuffle'== action:    # toggle use of a randomized playlist
                aud_handle.toggleshuffle()
            elif 'pl_repeat'== action:
                aud_handle.togglerepeat()
            elif 'volume_down'== action:
                aud_handle.lower_volume(AudmanagerServer.DEFAULT_VOL_DELTA)
            elif 'volume_up'== action:
                aud_handle.raise_volume(AudmanagerServer.DEFAULT_VOL_DELTA)

        if action is None:
            start_response('500 INTERNAL SERVER ERROR', [
                ('Content-Type', 'text/plain')])
            return ["Internal error: no action element in POST"]

        start_response('302 Found', [('Location', redir_url)])
        return []

    # process resource GET request; icons and images
    if path.endswith(".png") or path.endswith(".ico"): # image data files
        start_response('200 OK', [('Content-type', 'image/png'),
                                  ('cache-control', 'max-age=3600')])
        return file(resource_filename(__name__, path[1:]))

    # display player controls and status
    # extract input; size => show more/less, offset => scroll up/down
    tl_size = int(form_data.get('size', 
                                [AudmanagerServer.DEFAULT_TRACKLIST_LEN])[0])
    tl_offset = int(form_data.get('offset', [0])[0])
    # build the page
    active_pl_ind = -1
    active_pl_name = None
    playlists_lock = AudmanagerServer.playlists_locked
    if playlists_lock:
        active_pl_ind = -1
        active_pl_name = None
    else:
        try:      # older versions of audacious had no active playlist support
            active_pl_ind = aud_handle.getactiveplaylist()
            active_pl_name = aud_handle.getactiveplaylistname()
        except Exception, err:# 'org.freedesktop.DBus.Error.UnknownMethod'
            name = err.get_dbus_name()
            if name.startswith("org.freedesktop.DBus.Error.UnknownMethod"): 
                playlists_lock = True
            else:
                raise
    track_ind = aud_handle.position()
    length = 0
    current_title = codec = ""
    if track_ind > 0:           # else no track is selected
        length = aud_handle.songlength(track_ind)
        current_title = aud_handle.songtitle(track_ind)
        codec = codec_shortname(aud_handle.songtuple(track_ind, 'codec'))
    pl_max_ind = aud_handle.pl_length()
    if tl_size < 1: tl_size = 1     # minimum size
    new_offset = track_ind + tl_offset * tl_size * 2
    if new_offset < 0: 
        tl_offset += 1 
    elif new_offset > pl_max_ind: 
        tl_offset -= 1
    new_offset = track_ind + tl_offset * tl_size * 2
    play_list = aud_handle.pl_titles(new_offset, tl_size, tl_size,
                                     playlists_lock)
    seconds = aud_handle.time()
    volume = aud_handle.volume()
    state = aud_handle.player_status()
    (rate, freq, nch) = aud_handle.info() # out of sync during track change?
    audio_info = "%s %s, %s" \
                 % (codec, chn_form_shortname(nch),
                    "%02d kHz, %d kbps" % (freq/1000, rate/1000))
    is_repeat = aud_handle.is_repeat_mode()
    is_shuffle = aud_handle.is_shuffle_mode()
    if aud_handle.is_paused() or aud_handle.is_stopped():
        play_pause_icon = "ic_play_arrow_black_48dp.png"
    else: 
        play_pause_icon = "ic_pause_black_48dp.png" 
    play_lists = [] if playlists_lock else aud_handle.playlist_names()
    player_state = {     # page template arguments
        "hostname": socket.gethostname(),
        "current_title": current_title, "active_pl_name": active_pl_name, 
        "track_ind": track_ind, "active_pl_ind" : active_pl_ind,
        "track_length": length,
        "track_pos": seconds,
        "current_track_pos": "%02d:%02d/%02d:%02d" \
            % (seconds / 60, seconds % 60,
               length / 60, length % 60),
        "state": state, "volume": int(volume),
        "is_shuffle": is_shuffle, "is_repeat": is_repeat,
        "play_lists": play_lists,
        "audio_info": audio_info, "state_play_pause": play_pause_icon,
        "tracks": play_list, "playlists_lock": playlists_lock,
        "tl_size": tl_size, "tl_offset": tl_offset, "pl_mode": pl_mode
    }
    response_body = AudmanagerServer.tr_list.render(**player_state)
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html;charset=utf8'),
                        ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]

def usage(args):                # option help
    print ('usage: %s [-p <port>] [--port=<port>] [-e] [--enque] '
           + '[-l] [--playlists_locked]') %  args[0]

def main(args):                 # run the server and shutdown on signal
    signal.signal(signal.SIGTERM, AudmanagerServer.clean_exit)
    signal.signal(signal.SIGHUP, AudmanagerServer.clean_exit)
    try:
        runaudws(sys.argv)
    except KeyboardInterrupt:
        AudmanagerServer.clean_exit()
def runaudws(args):             # run the server
    hostname = ''
    port = 8051
    pl_mode = "play"
    playlists_locked = False
    try:
        opts, args = getopt.getopt(args[1:], "ep:l", ["enque", "port=",
                                                      "playlists_locked"])
    except getopt.GetoptError as err:
        print str(err)
        usage(args)
        sys.exit(2)    
    for o, a in opts:
        if o in ("-p" "--port"):
            port = int(a)
        elif o in ("-e", "--enque"):
            pl_mode = "enque"
        elif o in ("-l", "--playlists_locked"):
            playlists_locked = True

    # the ip detection might not pick a routable address (eg localhost)
    # maybe_ip = socket.gethostbyname(socket.gethostname()) # can return lo:
    maybe_ip = guess_listening_addr() 
    # Instantiate the WSGI server.
    # It will receive requests, pass it to the application
    # and send the application's responses back to the client
    server = AudmanagerServer((maybe_ip, port), application,
                               handler_class=LogErrorHandler)
    AudmanagerServer.default_pl_mode = pl_mode
    AudmanagerServer.playlists_locked = playlists_locked
    print "Audman: Audacious Audio Player Control listening on http://%s:%d" \
        % (maybe_ip, port)
    t = threading.Thread(target=server.serve_forever)
    t.start()
    while True:
        t.join(0.3)
        if not t.isAlive():     # allow shutdown on signal
            break
    AudmanagerServer.kill_thread.join()      
    # allow port to close to prevent
    # socket.error: [Errno 98] Address already in use
    del server
    print "restarting"
    os.execl(sys.executable, sys.executable, * sys.argv) # no return

if __name__ == '__main__':
    main(sys.argv)
