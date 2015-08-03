import speech_recognition as sr
from espeak import espeak
import time, pygame


def godcomplex():
	with sr.Microphone() as mic:
		rec=sr.Recognizer()
		#mic=sr.Microphone()
		rec.adjust_for_ambient_noise(mic)
		while True:
			print "listening"
			audio=rec.listen(mic)
			print "heard you"
			try:
				trans=str(rec.recognize(audio)).lower()
				print "you said "+trans
				if "god" in trans:
					espeak.synth("I believe you said my name")
					#time.sleep(2)
			except LookupError:
				print "did not get that"

def batmancomplex():
	pygame.mixer.init()
	pygame.mixer.music.load("/usr/local/lib/python2.7/dist-packages/godcomplex/batman.mp3")
	with sr.Microphone() as mic:
		rec=sr.Recognizer()
		rec.adjust_for_ambient_noise(mic)
		while True:
			print "listening"
			audio=rec.listen(mic)
			print "heard you"
			try:
				trans=str(rec.recognize(audio)).lower()
				print "you said "+trans
				if 'batman' in trans or 'gotham' in trans or 'joker' in trans or 'robin' in trans or 'bat' in trans:
					pygame.mixer.music.play()
					while pygame.mixer.music.get_busy()==True:
						continue
			except LookupError:
				print "did not get that"

def swearcomplex():
	pygame.mixer.init()
	pygame.mixer.music.load("/usr/local/lib/python2.7/dist-packages/godcomplex/daffy_language.mp3")
	with sr.Microphone() as mic:
		rec=sr.Recognizer()
		rec.adjust_for_ambient_noise(mic)
		while True:
			print "listening"
			audio=rec.listen(mic)
			print "heard you"
			try:
				trans=str(rec.recognize(audio)).lower()
				print "you said "+trans
				if "*" in trans: #since it censors itself
					pygame.mixer.music.play()
					while pygame.mixer.music.get_busy()==True:
						continue
			except:
				print "did not get that"

if __name__=="__main__":
	godcomplex()
