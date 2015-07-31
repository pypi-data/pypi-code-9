from acemorse import MorseCode

morse = MorseCode()

text = 'Hello world!'

print('Original text: {}'.format(text))
message = morse.generate(text)

print('Morse code: {}'.format(message))
translate = morse.translate(message)

print('Back to English: {}'.format(translate))
