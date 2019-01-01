# -*- encoding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from pyrollcall.database import Database
from pyrollcall.course import Course
from pyrollcall.student import Student
from pyrollcall.session import Session
import pyrollcall.face as face


class MainWindow(Gtk.Window):
    """ The main window of pyrollcall """
    def __init__(self):
        Gtk.Window.__init__(self, title="pyrollcall")
        self.set_border_width(10)
        self.set_size_request(200, 100)

        self.database = None 
        self.session = None
        self.session_list_store = Gtk.ListStore(str, str, bool)
        
        # Create a notebook.
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.init_rollcall_page()
        self.init_edit_page()
        self.init_about_page()


    def init_rollcall_page(self):
        # Create the rollcall page.
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
    
        self.session_list_store = Gtk.ListStore(str, str, bool)
        session_tree_view = Gtk.TreeView(self.session_list_store)

        for i, col_title in enumerate(["Student ID", "Name", "Arrived"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            column.set_sort_column_id(i)
            session_tree_view.append_column(column)

        content_row = Gtk.ListBoxRow()
        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        content_row.add(content_box)
        content_box.pack_start(session_tree_view, True, True, 0)
        listbox.add(content_row)
        self.notebook.append_page(listbox, Gtk.Label('Roll Call'))
        

    def init_edit_page(self):
        # Create the edit page.
        self.edit_page = Gtk.Box(margin=20)
        self.edit_page.set_border_width(10)

        create_course_button = Gtk.Button("New Course")
        create_course_button.connect("clicked", self.create_course)
        self.edit_page.add(create_course_button)

        create_student_button = Gtk.Button("New Student")
        create_student_button.connect("clicked", self.create_student)
        self.edit_page.add(create_student_button)

        train_model_button = Gtk.Button("Train Model")
        train_model_button.connect("clicked", self.train_model)
        self.edit_page.add(train_model_button)

        self.notebook.append_page(self.edit_page, Gtk.Label('Edit Courses/Students'))


    def init_about_page(self):
        # Create the about page.
        self.about_page = Gtk.Box()
        self.about_page.set_border_width(10)
        self.about_page.add(Gtk.Label("pyrollcall by aesophor"))
        self.notebook.append_page(self.about_page, Gtk.Label('About'))


    def update_session_tree_view(self):
        if self.session is None:
            return

        self.session_list_store.clear()
        for student, arrived in self.session.students_arrival.items():
            self.session_list_store.append([student.id, student.name, arrived])

    def connect_db(self, database):
        self.database = database

        c = Course(1071, 'Image Processing')
        s1 = Student('U10516045', 'Marco Wang')
        s2 = Student('U10516046', 'Tsai')
        s3 = Student('U10516001', 'John')
        c.add_student([s1, s2, s3])

        self.database.courses[0] = c

        self.session = Session(c)
        self.update_session_tree_view()


    def create_course(self, widget):
        form_dialog = FormDialog(self, title="Create New Course", message="Create New Course...")
        year_entry = form_dialog.add_entry("Class Year")
        name_entry = form_dialog.add_entry("Class Name")
        response = form_dialog.run()

        if response == Gtk.ResponseType.OK:
            print('OK Clicked, creating course')
            print(year_entry.get_text())
            print(name_entry.get_text())

        form_dialog.destroy()


    def create_student(self, widget):
        pass


    def train_model(self, widget):
        confirm_dialog = ConfirmDialog(self, title="Training Model", message="Are you sure?")
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            face.encode_faces(self.database, "faces/") # remove this hardcoded shit later
        
        confirm_dialog.destroy()


    def show(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()


class ConfirmDialog(Gtk.Dialog):
    """ Ask user to confirm the specified message """
    def __init__(self, parent, title="", message="", width=100, height=30):
        Gtk.Dialog.__init__(self, title, parent, Gtk.DialogFlags.MODAL, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        ))

        self.set_default_size(width, height)
        self.set_border_width(15)

        area = self.get_content_area()
        area.add(Gtk.Label(message))
        self.show_all()


class FormDialog(ConfirmDialog):
    """ Ask user to fill out the given form """
    def __init__(self, parent, title="", message="", width=100, height=50):
        ConfirmDialog.__init__(self, parent, title=title, message=message,
            width=width, height=height)

        self.listbox = Gtk.ListBox(margin=5)
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.get_content_area().add(self.listbox)
        self.show_all()

    def add_entry(self, title="", text=""):
        """ An entry in Gtk is like a text input area
        :param title: Displays a label on the LHS of the entry
        :param text: The default text in the entry
        :return: the reference to the entry we just created
        """
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        row.add(box)

        label = Gtk.Label(title)
        entry = Gtk.Entry()
        entry.set_text(text)

        box.pack_start(label, True, True, 0)
        box.pack_start(entry, True, True, 0)
        self.listbox.add(row)
        self.show_all()
        return entry
