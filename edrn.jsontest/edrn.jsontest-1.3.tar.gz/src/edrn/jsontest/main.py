import urllib2
import anyjson

def main():
    url = "http://jsonplaceholder.typicode.com/posts/1"
    response = urllib2.urlopen(url)
    data = anyjson.deserialize(response.read())
    print data['title']
