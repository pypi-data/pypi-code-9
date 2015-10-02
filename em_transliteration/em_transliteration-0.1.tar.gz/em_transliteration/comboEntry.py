#displaying the combobox outside the entry.  

#Python supports the creation of anonymous functions (i.e. functions that are not bound to a name) at runtime, using a construct called "lambda"

import gtk
'''
def clear_comboboxes(boxreference):
    try:
        while True:
            boxreference.remove_text(0)
    except:
        pass
    return
'''
def changed_cb(combobox):
    model = combobox.get_model()
    index = combobox.get_active()
    if index:
		#p=model[index][0]   ||This value could be taken in backend||
        print 'I choose', model[index][0]
    return

def on_key_press_event(widget, event):
	keyname = gtk.gdk.keyval_name(event.keyval)
	print keyname

	if keyname=="space":
        #get values to be displayed in the combobox from the backend.
		x="sejal"# x is the value coming from backend .	
        #for loop for the number of values being sent from backend
		combobox.append_text(x)
		combobox.connect('changed',changed_cb)
		combobox.set_active(0)
		combobox.show()
	else:	
		combobox.hide()

if __name__ == '__main__':
	window = gtk.Window()
	window.connect('destroy',lambda x: gtk.main_quit())
	entry = gtk.Entry()	
	combobox = gtk.combo_box_new_text()
	hbox=gtk.HBox()
	hbox.pack_start(entry)
	hbox.pack_start(combobox)
     
	window.add(hbox)
	window.connect('key_press_event', on_key_press_event)
	
	window.show_all()
	combobox.hide()
	gtk.main()
