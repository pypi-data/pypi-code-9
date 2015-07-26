from whatsapp import Client
import logging
logging.basicConfig(level=logging.ERROR)

to = '31641370305'

client = Client(login='31615161376', password='AgYZCNGgWYxhoeeH/Ngi3Pd0vr4=')
client.send_message(to, 'Monkey brain111')
client.send_media(to, path='/Users/paultax/Desktop/logo.jpg')
