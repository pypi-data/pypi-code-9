import pygtk
import gtk

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
	    combobox.set_active(1)
	    combobox.show()
    else:
	    combobox.hide()

if __name__ == '__main__':
    w  = gtk.Window()
    w.connect('destroy',lambda x: gtk.main_quit())
    combobox = gtk.combo_box_new_text()
    image=gtk.Image()
    image.set_from_file("text.jpeg")
    tv = gtk.TextView()
    hbox=gtk.HBox()
    hbox.pack_start(tv)
    hbox.pack_start(combobox)
    tv.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
    tv.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
    buffr = gtk.TextBuffer()
    buffr.set_text("WHATEVER TEXT")
    tv.connect('key_press_event', on_key_press_event)
    tv.set_buffer(buffr)
    w.add(hbox)
    w.show_all()
    combobox.hide()
    gtk.main()
