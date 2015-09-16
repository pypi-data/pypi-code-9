from sublimescheme.generate import *

# Needed to see all available scopes
# from sublimescheme.scopes import *

# Follow order of the following lines
make = Make("Cherry", "Daniel")
make.start()
make.head(fg="#000", bg="#FFFFFF", ct="#F00", inv="#0FF", lh="#004312", se="#eeffee", fh="#00BFFF", fhf="f0f0f0", sb="#E996F7", sg="#abcdef")

# Add extra scopes to your themes.
# You can add as many body as possible
#make.body('Ruby: Numbers', 'constant.numeric.ruby', fs='italic', fg='#f0f', bg='#0ff')

make.complete()
make.readme("github.com/me/cherry", "daniel@aol.com")
make.package("github.com/me/cherry")

# Use to check 161 available language scopes
# print(scopes)

#Use to check all available scopes for a programming language
#e.g. cpp() 
# or html()