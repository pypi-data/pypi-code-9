import gtk
from autoTransliterate.list_generator import *

str_buff = ''

def on_key_press_event(widget, event):
	global str_buff
	more_vals = True

	keyname = gtk.gdk.keyval_name(event.keyval)

	str_buff += keyname
	print str_buff

	if more_vals:
		generate(str_buff)
	# TODO: add code to query for available str_buff in database

if __name__ == '__main__':

	w = gtk.Window()
	entry = gtk.Entry()

	w.add(entry)
	w.connect('key_press_event', on_key_press_event)
	w.show_all()

	gtk.main()
