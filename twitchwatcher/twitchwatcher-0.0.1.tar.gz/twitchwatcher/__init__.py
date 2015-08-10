import sys
import os

def usage():
    """Print usage info and exit the app"""
    print("Usage: %s [stream_name | http://stream_url]" % sys.argv[0])
    sys.exit(2)

def normalize_stream_url(stream_url):
    """Makes a twitch stream url from a stream name (leaves urls as is)"""
    if stream_url.startswith("http://") or stream_url.startswith("https://"):
        return stream_url
    return "http://twitch.tv/%s" % stream_url

def main():
    if len(sys.argv) < 2:
        usage()

    stream_url = normalize_stream_url(sys.argv[1])
    print("Running stream: %s" % stream_url)
    app = "livestreamer"
    os.execvp(app, [app, stream_url, "best"] + sys.argv[2:])
