import music21
#us = environment.UserSettings()
#us.create()  
#sBach = corpus.parse('bach/bwv7.7')
#sBach.show()
#converter.parse('/Users/cuthbert/Desktop/Bach.xml',sBach)
#Music21File=converter.parse("tinynotation: 3/4 c4 d8 f g16 a g f#")



print(music21.note)

s=music21.stream.Stream()






#Music21File.show('text')
#print(Music21File._elements[1].__dict__)

#Music21File._elements[1].JJJ='noqsdqsdq'
#Music21File.write('musicxml',fp="./Music21.xml")

#a=vexflow.fromObject(Music21File,mode='html')

#help(vexflow.fromObject)


#print a.replace('CANVAS','SVG')


#Music21File.write('lilypond',fp="./Music21.ly")
#import os
#os.popen('/Applications/LilyPond.app/Contents/Resources/bin/lilypond -dbackend ./Music21.ly')


#help(Music21File.write)



"""
from MeteorClient import MeteorClient
ApiMeteorClient = MeteorClient('ws://127.0.0.1:3000/websocket')
ApiMeteorClient.connect()
print(ApiMeteorClient.ddp_client.call)
"""
"""
import ddp
# Create a client, passing the URL of the server.
client = ddp.ConcurrentDDPClient('ws://127.0.0.1:3000/websocket')
# Once started, the client will maintain a connection to the server.
client.start()
print(333)
future=client.call('upper',45)
#client.join()

# Block until the result message is received.
result_message = future.get()

# Check if an error occured else print the result.
if result_message.has_error():
	print result_message.error
else:
	print result_message.result

client.stop()
"""

"""
var zerorpc = require("zerorpc");
var client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");
client.invoke("hello", "World", function(error, reply, streaming) {
    if(error){
        console.log("ERROR: ", error);
    }
    console.log(reply);
});
"""