# -*- encoding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    """ The main window of pyrollcall """
    def __init__(self):
        Gtk.Window.__init__(self, title="pyrollcall")
        self.set_border_width(10)
        self.set_size_request(200, 100)
        
        # Create a notebook.
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        # Create the management page.
        listbox = Gtk.ListBox(margin=5)
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        header_row = Gtk.ListBoxRow()
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        header_row.add(header_box)

        start_button = Gtk.Button("Start")
        end_button = Gtk.Button("End")
        end_button.set_sensitive(False)
        sign_in_button = Gtk.Button("Sign In")
        header_box.pack_start(start_button, True, True, 0)
        header_box.pack_start(end_button, True, True, 0)
        header_box.pack_start(sign_in_button, True, True, 0)
        listbox.add(header_row)


        content_row = Gtk.ListBoxRow()
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        content_row.add(content_box)
        
        # add tree view here
        lbl = Gtk.Label("Placeholder for treeview")
        content_box.pack_start(lbl, True, True, 0)
        listbox.add(content_row)

        

        self.notebook.append_page(listbox, Gtk.Label('Roll Call'))
        
        # Create the Sign in page.
        self.sign_in_page = Gtk.Box()
        self.sign_in_page.set_border_width(10)
        self.sign_in_page.add(Gtk.Label("Yo2"))
        self.notebook.append_page(self.sign_in_page, Gtk.Label('Edit Courses/Students'))

        # Create the Result page.
        self.sign_in_page = Gtk.Box()
        self.sign_in_page.set_border_width(10)
        self.sign_in_page.add(Gtk.Label("This software is created by Marco Wang"))
        self.notebook.append_page(self.sign_in_page, Gtk.Label('About'))



window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()

Gtk.main()
