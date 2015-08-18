import sys
import os
import threading
# import signal
import asyncio
import time
import argparse

from queue import Queue

from .settings import Settings, default_settings_file, settings

import lyricscreen

parser = argparse.ArgumentParser(description="A lyrics management and display web app and server")

parser.add_argument("-v", "--version", action="version", version="LyricScreen v" + lyricscreen.__version__)
parser.add_argument("-vv", "--verbose", help="show all available program output", action="store_true")
parser.add_argument("--default-config", help="display the default config file", action="store_true")
parser.add_argument("--show-config", help="print the values of the given or default config file", action="store_true")
parser.add_argument("--create-config", help="create the default config file", action="store_true")
# parser.add_argument("--copy-web-client", help="copy the web client files to the specified location", nargs="?", default="./lyricscreen_web_client")
parser.add_argument("--suppress-browser-window", help="prevent the browser window from opening on startup", action="store_true")
parser.add_argument("CONFIG", help="the .json file to load config variables from", nargs="?", default=default_settings_file)

def main():
    # Handle some cli flags
    args = parser.parse_args()

    # Show default config contents
    if args.default_config:
        settings = Settings('')
        print(settings.settings_json())
        sys.exit(0)

    from .wsserver import WebSocketServer
    from .httpserver import WebClientServer, web_root

    if not os.path.isfile(os.path.join(web_root, "console.html")):
        print("No web client detected in current web_client_dir - symlinking default client")
        import shutil
        default_web_client_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "http"))
        print(default_web_client_dir)
        print(web_root)
        if os.path.isdir(web_root):
          print("The web client directory exists ({}), but without a console.html file - we moved it it to {} so we could copy the default web client there.".format(web_root, web_root + "_saved"))
          shutil.move(web_root, web_root + "_saved")
        os.symlink(default_web_client_dir, os.path.abspath(web_root), True)

    # Create default config
    if args.create_config:
        settings = Settings('')
        settings.save(default_settings_file)
        print("Created config file at %s" % settings.file)
        sys.exit(0)

    settings = Settings(args.CONFIG)

    # Show current config settings
    if args.show_config:
        print(settings.settings_json())
        sys.exit(0)

    if args.verbose:
        settings.verbose = True
        print("Command line arguments:")
        print("    ", args)

    if not os.path.isdir(settings.data_dir):
        os.makedirs(settings.data_dir)

    songs_dir = os.path.join(settings.data_dir, settings.songs_dir)
    if not os.path.isdir(songs_dir):
        os.makedirs(songs_dir)

    playlists_dir = os.path.join(settings.data_dir, settings.playlists_dir)
    if not os.path.isdir(playlists_dir):
        os.makedirs(playlists_dir)

    print("Data Directory: {}".format(settings.data_dir))
    print("Web Client Directory: {}".format(web_root))

    # Get event loop for websocket server
    loop = asyncio.get_event_loop()

    # Create server objects
    websocket_server = WebSocketServer(loop=loop)
    http_server = WebClientServer()

    # Create server threads
    websocket_server_thread = threading.Thread(target=websocket_server.start)
    http_server_thread = threading.Thread(target=http_server.start)
    websocket_server_thread.daemon = True
    http_server_thread.daemon = True

    # Start threads
    websocket_server_thread.start()
    http_server_thread.start()

    # Open browser to console page (with login info?)
    if not args.suppress_browser_window:
        import webbrowser
        if settings.verbose:
            print("Opening browser...")
        url = "http://localhost:" + str(http_server.port) + "/console"
        webbrowser.open(url)

    # Create thread queue
    q = Queue()

    # Put threads in queue
    q.put(websocket_server_thread)
    q.put(http_server_thread)

    # Run async event loop
    time.sleep(0.1)
    loop.run_until_complete(websocket_server.sock)
    loop.run_forever()

    # Halt program until threads have run
    q.join()

