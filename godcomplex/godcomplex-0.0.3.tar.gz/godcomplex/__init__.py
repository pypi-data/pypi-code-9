import speech_recognition as sr
from espeak import espeak
import time

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

if __name__=="__main__":
	godcomplex()
