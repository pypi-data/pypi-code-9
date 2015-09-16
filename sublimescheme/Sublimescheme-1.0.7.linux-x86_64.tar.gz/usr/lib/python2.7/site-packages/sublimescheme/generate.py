import os

_about = "A Vibrant Sublime text 2 and 3 Color Scheme"

def _write(filename, text, value):
	filename.write("\t\t\t\t<key>{}</key>\n\t\t\t\t<string>{}</string>\n".format(text, value))

class Make():
	def __init__(self, maindir, author=""):
		self.maindir = maindir
		self.author = author
		# Directory paths
		self.mypath = os.getcwd() 
		self.themedir = (self.mypath + "/" + self.maindir)

		#Create folder if not present
		if not os.path.exists(self.themedir): os.mkdir(self.themedir)
		print(self.maindir + " folder created in current working directory")

		self.filename = self.maindir + '.tmTheme'  # Name of file 
		self.filepath = os.path.join(self.themedir,self.filename)

		self.file = open(self.filepath,'w') 
		self.file.close()

		print(str(maindir) +"/" + str(self.filename) + " created. Feel free to rename it\n")
		print("TODO: call .start() on class instance\n")


	def start(self):
		ln1 = ('\n<?xml version="1.0" encoding="UTF-8"?>\n')
		ln2 = ('<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
		ln3 = ('<plist version="1.0">\n<dict>\n')
		ln4 = ('\t<key>author</key> \n\t<string>{}</string>\n'.format(self.author))
		ln5 = ('\t<key>name</key>\n\t<string>{}</string>\n'.format(self.maindir))
		ln6 = ('\t<key>settings</key>\n\t<array>\n\t')
		ln7 = "\t<dict>\n\t"
		ln8 = "\t\t<key>settings</key>\n\t"
		ln9 = "\t\t<dict>\n"

		lines = [ln1, ln2, ln3, ln4, ln5, ln6, ln7, ln8, ln9]
		self.file = open(self.filepath,'w') 

		for x in lines:
			self.file.write(x)
		self.file.close()

		print("Main xml heading written")
		print("TODO: Call .head() on class instance with any params and values")
		print("e.g. instance.head(fg='#F0F', bg='#0FF')\n")
		print("options are:\n\tag --> activeGuide")
		print("\tbg --> background")
		print("\tct --> caret")
		print("\tfg --> foreground")
		print("\tfh --> findHighlight")
		print("\tfhf --> findHighlightForeground")
		print("\tgf --> gutterForeground")
		print("\tgu --> guide")
		print("\tgut --> gutter")
		print("\tins --> inactiveSelection")
		print("\tinv --> invisibles")
		print("\tlh --> lineHighlight")
		print("\tsb --> selectionBorder")
		print("\tse --> selection")
		print("\tsg --> stackGuide\n")


	def head(self, **options):
		self.file = open(self.filepath,'a') 

		for x in sorted(options):
			if x == "ag":
				_write(self.file, "activeGuide", options[x])

			if x == "bg":
				_write(self.file, "background", options[x])

			if x == "ct":
				_write(self.file, "caret", options[x])

			if x == "fg":
				_write(self.file, "foreground", options[x])

			if x == "fh":
				_write(self.file, "findHighlight", options[x])

			if x == "fhf":
				_write(self.file, "findHighlightForeground", options[x])

			if x == "gf":
				_write(self.file, "gutterForeground", options[x])

			if x == "gu":
				_write(self.file, "guide", options[x])

			if x == "gut":
				_write(self.file, "gutter", options[x])


			if x == "ins":
				_write(self.file,"inactiveSelection", options[x])

			if x == "inv":
				_write(self.file,"invisibles", options[x])
			
			if x == "lh":
				_write(self.file, "lineHighlight", options[x])

			if x == "sb":
				_write(self.file,"selectionBorder", options[x])

			if x == "se":
				_write(self.file,"selection", options[x])

			if x == "sg":
				_write(self.file, "stackGuide", options[x])

		self.file.write("\t\t\t</dict>\n\t\t</dict>\n")

		self.body("Comment", "comment", fg="#919191")
		self.body("String", "string", fg="#00A33F")
		self.body("Number", "constant.numeric") 
		self.body("Built-in constant", "constant.language", fg="#A535AE")
		self.body("User-defined constant", "constant.character, constant.other")
		self.body("Variable", "variable.language, variable.other")
		self.body("Keyword", "keyword", fg="#FF5600")
		self.body("Storage", "storage", fg="#FF5600")
		self.body("Type name", "entity.name.type", fg="#21439C")
		self.body("Inherited class", "entity.other.inherited-class")
		self.body("Function name", "entity.name.function", fg="#21439C")
		self.body("Function argument", "variable.parameter")
		self.body("Tag name", "entity.name.tag")
		self.body("Tag attribute", "entity.other.attribute-name")
		self.body("Library function", "support.function", fg="#A535AE")
		self.body("Library constant", "support.constant", fg="#A535AE")
		self.body("Library class/type", "support.type, support.class", fg="#A535AE")
		self.body("Library variable", "support.variable", fg="#A535AE")
		self.body("Invalid", "invalid", bg="#990000", fg="#FFFFFF")
		self.body("String interpolation", "constant.other.placeholder.py", fs="", fg="#990000")
		

		print("IDLE look-alike generated but you can add more customization to your file\n")
		print("TODO: call .body() on your class instance with arguments:")
		print("\tinstance.body('description','language scope', 'optional: text decoration')\n")
		print("e.g. instance.body('Ruby: Comments', 'constant.numeric.ruby', fs='bold italic', fg='#f0f')\n")

	def body(self, desc, scope, **options):
		ln1 = "\n\t\t<dict>"
		ln2 = "\n\t\t\t<key>name</key>"
		ln3 = "\n\t\t\t<string>{}</string>".format(desc.title())
		ln4 = "\n\t\t\t<key>scope</key>"
		ln5 = "\n\t\t\t<string>{}</string>".format(scope)
		ln6 = "\n\t\t\t<key>settings</key>"
		ln7 = "\n\t\t\t<dict>\n"

		lnend = "\t\t\t</dict>\n\t\t</dict>\n"

		if (len(options)) == 0:
			ln7 = "\n\t\t\t<dict/>\n"
			lnend = "\t\t</dict>\n"

		lines = [ln1, ln2, ln3, ln4, ln5, ln6, ln7]

		for x in lines:
			self.file.write(x)

		for x in sorted(options):
			if x == "bg":
				_write(self.file, "background", options[x].upper())

			if x == "fg":
				_write(self.file, "foreground", options[x].upper())

			if x == "fs":
				_write(self.file, "fontStyle", options[x])


		self.file.write(lnend)

	def complete(self, uuid="c5873966-71ae-43da-8711-a22542e06922"):
		ln1 = ('\n\t</array>\n')
		ln2 = ('\t<key>uuid</key>\n\t<string>{}</string>\n'.format(uuid))
		ln3 = ('</dict>\n</plist>')
		
		lines = [ln1, ln2, ln3]
		self.file = open(self.filepath,'a') 

		for x in lines:
			self.file.write(x)
		self.file.close()

		print("\nCongratulations. Color Scheme completed")
		print("\nTODO: call .readme() on your class instance to generate a README file\nArguments are ('repository URL', 'email address', 'screenshot image filename'). \n\nYou can leave all the arguments blank like this '' for each of them if you don't want to supply any but it's advisable to supply them.\nMake sure the image is in the safe folder as the generated README.md file")


	def readme(self, link="", email="", screenshot=""):

		title = "\n# {} Sublime Color Scheme\n\n".format(self.maindir)

		img = "\n"
		if len(screenshot) > 4:
			img = "## Screenshot\n![{} Screenshot preview](./{})\n\n".format(self.maindir, screenshot)

		about = "## About\n{}\n\n".format(_about)
		inst = "## Installation\nOpen `Tools -> Command Palette...`. Search for `Package Control: Install Package` and click enter. Wait for the available packages to show up and then search for `{}`. Click enter and the color scheme should be installed.\n\n".format(self.maindir)

		# Check whether to add a contribution header.
		contrb = ""
		if len(link) >= 5:
			contrb = "## Contributing\nAll contributions are welcome. You can fork me on {}\n\n".format(link) 
		else:
			contrib = "\n"
			
		licsn = "## License\n\nMIT (c) 2015 {} | {}\n\nThis is free software. It is licensed under the MIT License. Feel free to use this in your own work. However, if you modify and/or redistribute it, please attribute me in some way, and it would be great if you distribute your work under this or a similar license, but it's not required.\n\n".format(self.author, email)

		ack = "## Acknowledgements\n\nCreated using [sublimescheme](https://pypi.python.org/pypi/Sublimescheme) package for Python by [Taiwo Kareem](https://github.com/tushortz). An alternative for Ruby programming language is [Sublimetheme](https://rubygems.org/gems/sublimetheme). \n\nAll glory honour and adoration belongs to God alone.\n\n"


		lines = [title, img, about, inst, contrb, licsn, ack]

		filename = 'README.md'   
		filepath = os.path.join(self.themedir, filename)

		file_ = open(filepath,'w')

		for x in lines:
			file_.write(x)
		file_.close()
		print("\nREADME.md file created. Feel free to customize it.\n")
		
	def package(self, repo, ):
		ln0 = "// If you intend to publish it on packagecontrol.io, then copy the following code into the forked repository and paste it in the corresponding repository folder.\n\n"
		ln1 = '{} \n\t"name": "{}",'.format('{', self.maindir)
		ln2 = '\n\t"details": "{}",'.format(repo)
		ln3 = '\n\t"labels": ["color scheme","highlighting","linting"],'
		ln4 = '\n\t"releases": ['
		ln5 = '\n\t\t{}'.format('{')
		ln6 = '\n\t\t\t"sublime_text": "*",'
		ln7 = '\n\t\t\t"tags": true'
		ln8 = '\n\t\t{}\n\t{}\n{}{}'.format('}', ']', '}', '  //,')

		lines = [ln0, ln1, ln2, ln3, ln4, ln5, ln6, ln7, ln8]

		filename = 'packages.json'   
		filepath = os.path.join(self.themedir, filename)

		file_ = open(filepath,'w')

		for x in lines:
			file_.write(x)
		file_.close()

		print("Packages.json file created. Check it to make sure it contains the right data")
