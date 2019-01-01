# -*- encoding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from enum import IntEnum
from pyrollcall.database import Database
from pyrollcall.course import Course
from pyrollcall.student import Student
from pyrollcall.session import Session
import pyrollcall.face as face


class DataType(IntEnum):
    COURSE = 0
    STUDENT = 1


class MainWindow(Gtk.Window):
    """ The main window of pyrollcall """
    def __init__(self):
        Gtk.Window.__init__(self, title="pyrollcall")
        self.set_wmclass("pyrollcall", "pyRollCall")
        self.set_border_width(10)
        self.set_default_geometry(640, 480)
        self.set_size_request(200, 100)

        self.database = None 
        self.session = None

        self.start_rollcall_btn = Gtk.Button("Start")
        self.end_rollcall_btn = Gtk.Button("End")
        self.sign_in_btn = Gtk.Button("Sign In")
        self.session_tree_view = None
        self.current_rollcall_course_label = Gtk.Label("No ongoing rollcall.")

        self.manage_page_notebook = None
        self.courses_tree_view = None
        self.students_tree_view = None

        # Create the primary notebook (tabbed pane).
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        # Initialize pages (tabs) in the primary notebook.
        self.init_rollcall_page()
        self.init_edit_page()


    def init_rollcall_page(self):
        # Create the rollcall page.
        listbox = Gtk.ListBox(margin=5)
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        header_row = Gtk.ListBoxRow()
        header_row.add(header_box)
        listbox.add(header_row)

        self.start_rollcall_btn.connect("clicked", self.start_rollcall)

        self.end_rollcall_btn.connect("clicked", self.stop_rollcall)
        self.end_rollcall_btn.set_sensitive(False)

        self.sign_in_btn.connect("clicked", self.sign_in)
        self.sign_in_btn.set_sensitive(False)

        header_box.pack_start(self.start_rollcall_btn, True, True, 0)
        header_box.pack_start(self.end_rollcall_btn, True, True, 0)
        header_box.pack_start(self.sign_in_btn, True, True, 0)

        banner_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        banner_row = Gtk.ListBoxRow()
        banner_row.add(banner_box)
        listbox.add(banner_row)
    
        banner_box.pack_start(self.current_rollcall_course_label, True, True, 0)

        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        content_row = Gtk.ListBoxRow()
        content_row.add(content_box)
        listbox.add(content_row)

        self.session_tree_view = TreeView(Gtk.ListStore(str, str, bool), ["ID", "Name", "Arrived"])
        content_box.pack_start(self.session_tree_view, True, True, 0)
        
        self.notebook.append_page(listbox, Gtk.Label('Roll Call'))       

    def init_edit_page(self):
        # Create the edit page.
        listbox = Gtk.ListBox(margin=5)
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        header_row = Gtk.ListBoxRow()
        header_row.add(header_box)
        listbox.add(header_row)

        create_btn = Gtk.Button("Create")
        create_btn.connect("clicked", self.on_create_btn_clicked)
        
        edit_btn = Gtk.Button("Edit")
        edit_btn.connect("clicked", self.on_edit_btn_clicked)
        
        remove_btn = Gtk.Button("Remove")
        remove_btn.connect("clicked", self.on_remove_btn_clicked)

        take_photos_btn = Gtk.Button("Take Photos")
        take_photos_btn.connect("clicked", self.on_take_photos_btn_clicked)

        train_model_btn = Gtk.Button("Train Model")
        train_model_btn.connect("clicked", self.on_train_model_btn_clicked)

        header_box.pack_start(create_btn, True, True, 0)
        header_box.pack_start(edit_btn, True, True, 0)
        header_box.pack_start(remove_btn, True, True, 0)
        header_box.pack_start(take_photos_btn, True, True, 0)
        header_box.pack_start(train_model_btn, True, True, 0)


        content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        content_row = Gtk.ListBoxRow()
        content_row.add(content_box)
        listbox.add(content_row)

        # Display all courses and students in the database in two different tabs resp.
        self.manage_page_notebook = Gtk.Notebook()
        courses_listbox = Gtk.ListBox(margin=5)
        courses_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        students_listbox = Gtk.ListBox(margin=5)
        students_listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        # Courses page.
        courses_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        courses_row = Gtk.ListBoxRow()
        courses_row.add(courses_box)
        courses_listbox.add(courses_row) 
        self.courses_tree_view = TreeView(Gtk.ListStore(int, str, str), ["id", "Year", "Name"])
        if self.database is not None:
            self.courses_tree_view.bind(self.database.courses)
        courses_box.pack_start(self.courses_tree_view, True, True, 0)

        # Students page.
        students_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        students_row = Gtk.ListBoxRow()
        students_row.add(students_box)
        students_listbox.add(students_row) 
        self.students_tree_view = TreeView(Gtk.ListStore(str, str), ["id", "Name"])
        if self.database is not None:
            self.students_tree_view.bind(self.database.students)
        students_box.pack_start(self.students_tree_view, True, True, 0)

        self.manage_page_notebook.append_page(courses_listbox, Gtk.Label('All Courses'))
        self.manage_page_notebook.append_page(students_listbox, Gtk.Label('All Students'))
        content_box.pack_start(self.manage_page_notebook, True, True, 0)        

        self.notebook.append_page(listbox, Gtk.Label('Manage Courses/Students'))


    def update_session_tree_view(self):
        if self.session is None:
            return

        self.session_tree_view.list_store.clear()
        for student, arrived in self.session.students_arrival.items():
            self.session_tree_view.list_store.append([student.id, student.name, arrived])


    def connect_db(self, database):
        self.database = database
        self.courses_tree_view.bind(self.database.courses)
        self.students_tree_view.bind(self.database.students)


    def start_rollcall(self, widget):
        form_dialog = FormDialog(self, title="Start a Roll Call", message="Which one is your class today?")
        # Add a student tree view to the dialog.
        courses_list_store = Gtk.ListStore(int, str, str)
        courses_tree_view = TreeView(courses_list_store, ["ID", "Semester", "Name"], Gtk.SelectionMode.MULTIPLE)
        form_dialog.add_tree_view(courses_tree_view, title="Courses")
        courses_tree_view.bind(self.database.courses)
        response = form_dialog.run()

        if response == Gtk.ResponseType.OK:
            selected_course_id = courses_tree_view.get_selected_items()[0]
            selected_course = self.database.get_course(selected_course_id)
            # Initiate a new rollcall session using the selected course.
            self.session = Session(selected_course)
            self.start_rollcall_btn.set_sensitive(False)
            self.end_rollcall_btn.set_sensitive(True)
            self.sign_in_btn.set_sensitive(True)
            self.update_session_tree_view()
            self.current_rollcall_course_label.set_text("Current roll call: ({}) {}".format(
                selected_course.year, selected_course.name))
            

        form_dialog.destroy()

    def stop_rollcall(self, widget):
        confirm_dialog = ConfirmDialog(self, title="End Roll Call", message="End current roll call?")
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.session.export()
            self.session = None
            self.start_rollcall_btn.set_sensitive(True)
            self.end_rollcall_btn.set_sensitive(False)
            self.sign_in_btn.set_sensitive(False)
            self.current_rollcall_course_label.set_text("No ongoing rollcall.")

        confirm_dialog.destroy()


    def sign_in(self, widget):
        form_dialog = FormDialog(self, title="Sign in", message="Please enter your student ID")
        id_entry = form_dialog.add_entry("Student ID")
        response = form_dialog.run()

        if response == Gtk.ResponseType.OK:
            img_path = face.collect_faces()[0]
            student_id = face.recognize_face(self.database, img_path)[0]

            if student_id == id_entry.get_text().upper():
                self.session.mark_as_arrived(student_id)
                self.update_session_tree_view()

        form_dialog.destroy()


    def on_create_btn_clicked(self, widget):
        if self.manage_page_notebook.get_current_page() == DataType.COURSE:
            self.create_course()
        elif self.manage_page_notebook.get_current_page() == DataType.STUDENT:
            self.create_student()

    def on_edit_btn_clicked(self, widget):
        if self.manage_page_notebook.get_current_page() == DataType.COURSE:
            # The selection model of courses tree view is SINGLE,
            # so we'll try to get the first item in the list.
            selected_course_id = self.courses_tree_view.get_selected_items()[0]
            selected_course = self.database.get_course(selected_course_id)
            self.edit_course(selected_course)
        elif self.manage_page_notebook.get_current_page() == DataType.STUDENT:
            selected_student_id = self.students_tree_view.get_selected_items()[0]
            selected_student = self.database.get_student(selected_student_id)
            self.edit_student(selected_student)

    def on_remove_btn_clicked(self, widget):
        if self.manage_page_notebook.get_current_page() == DataType.COURSE:
            selected_course_id = self.courses_tree_view.get_selected_items()[0]
            selected_course = self.database.get_course(selected_course_id)
            self.remove_course(selected_course)
        elif self.manage_page_notebook.get_current_page() == DataType.STUDENT:
            selected_student_id = self.students_tree_view.get_selected_items()[0]
            selected_student = self.database.get_student(selected_student_id)
            self.remove_student(selected_student)
    
    def on_take_photos_btn_clicked(self, widget):
        selected_students_ids = self.students_tree_view.get_selected_items()

        if len(selected_students_ids) > 0:
            selected_student_id = selected_students_ids[0]
            selected_student = self.database.get_student(selected_student_id)
            
            form_dialog = FormDialog(self, title="Take Photos", message="Click OK and Press SPACE to take photos")
            photo_count_entry = form_dialog.add_entry("Number of Photos")
            photo_count_entry.set_text("5") # remove this hardcoded shit later
            response = form_dialog.run()

            if response == Gtk.ResponseType.OK:
                face.collect_faces(selected_student, img_count=int(photo_count_entry.get_text()))
            form_dialog.destroy()

    def on_train_model_btn_clicked(self, widget):
        confirm_dialog = ConfirmDialog(self, title="Training Model", message="Are you sure?")
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            face.encode_faces(self.database, "faces/") # remove this hardcoded shit later
            self.database.dump()
        
        confirm_dialog.destroy()



    def create_course(self):
        form_dialog = FormDialog(self, title="Create New Course", message="Create New Course...")
        # Add year and name entries to the dialog.
        year_entry = form_dialog.add_entry("Semester")
        name_entry = form_dialog.add_entry("Class Name")
        # Add a student tree view to the dialog.
        students_list_store = Gtk.ListStore(str, str)
        students_tree_view = TreeView(students_list_store, ["ID", "Name"], Gtk.SelectionMode.MULTIPLE)
        form_dialog.add_tree_view(students_tree_view, title="Students")
        students_tree_view.bind(self.database.students)

        response = form_dialog.run()

        if response == Gtk.ResponseType.OK:
            c = self.database.add_course(year_entry.get_text(), name_entry.get_text())
            selected_items = students_tree_view.get_selected_items()
            for student_id in selected_items:
                s = self.database.get_student(student_id)
                c.add_student(s)
            self.courses_tree_view.bind(self.database.courses)
            self.database.dump()

        form_dialog.destroy()

    def edit_course(self, course: Course):
        form_dialog = FormDialog(self, title="Edit Course", message="Edit Course...")
        # Add year and name entries to the dialog.
        year_entry = form_dialog.add_entry("Semester")
        name_entry = form_dialog.add_entry("Class Name")
        year_entry.set_text(course.year)
        name_entry.set_text(course.name)

        # Add a student tree view to the dialog.
        students_list_store = Gtk.ListStore(str, str)
        students_tree_view = TreeView(students_list_store, ["ID", "Name"], Gtk.SelectionMode.MULTIPLE)
        form_dialog.add_tree_view(students_tree_view, title="Students")
        students_tree_view.bind(self.database.students)

        # Automatically selects (toggles) the students within this course.
        students_tree_view.get_selection().select_all()
        model, rows = students_tree_view.get_selection().get_selected_rows()
        for row in rows:
            tree_iter = model.get_iter(row)
            primary_key = model.get_value(tree_iter, 0)
            found = False
            for student in course.students:
                if student.id == primary_key:
                    found = True
            if found is False:
                students_tree_view.get_selection().unselect_path(row)

        response = form_dialog.run()

        if response == Gtk.ResponseType.OK:
            course.year = year_entry.get_text()
            course.name = name_entry.get_text()
            selected_items = students_tree_view.get_selected_items()

            course.students.clear()
            for student_id in selected_items:
                s = self.database.get_student(student_id)
                course.add_student(s)
            self.courses_tree_view.bind(self.database.courses)
            self.database.dump()

        form_dialog.destroy()

    def remove_course(self, course: Course):
        confirm_dialog = ConfirmDialog(self, title="Remove Course", message="Remove {} {}?".format(
            course.year, course.name))
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.database.remove_course(course)
            self.courses_tree_view.bind(self.database.courses)
            self.database.dump()
        
        confirm_dialog.destroy()



    def create_student(self):
        form_dialog = FormDialog(self, title="Create New Student", message="Create New Student...")
        id_entry = form_dialog.add_entry("Student ID")
        name_entry = form_dialog.add_entry("Student Name")
        response = form_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.database.add_student(id_entry.get_text(), name_entry.get_text())
            self.students_tree_view.bind(self.database.students)
            self.database.dump()

        form_dialog.destroy()

    def edit_student(self, student: Student):
        form_dialog = FormDialog(self, title="Edit Student", message="Edit Student...")
        id_entry = form_dialog.add_entry("Student ID")
        name_entry = form_dialog.add_entry("Student Name")
        id_entry.set_sensitive(False)
        id_entry.set_text(student.id)
        name_entry.set_text(student.name)
        response = form_dialog.run()

        if response == Gtk.ResponseType.OK:
            student.id = id_entry.get_text()
            student.name = name_entry.get_text()
            self.students_tree_view.bind(self.database.students)
            self.database.dump()

        form_dialog.destroy()

    def remove_student(self, student: Student):
        confirm_dialog = ConfirmDialog(self, title="Remove Student", message="Remove {} {}?".format(
            student.id, student.name))
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.database.remove_student(student)
            self.students_tree_view.bind(self.database.students)
            self.database.dump()
        
        confirm_dialog.destroy()




    def show(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()




""" Move the bitches below to another motherfucking module """

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
        :return: The reference to the entry we just created
        """
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        row.add(box)

        label = Gtk.Label(title)
        entry = Gtk.Entry()
        entry.set_text(text)

        box.pack_start(label, True, True, 0)
        box.pack_start(entry, True, True, 0)
        self.listbox.add(row)
        self.show_all()
        return entry

    def add_tree_view(self, tree_view, title=""):
        """ Add a TreeView 
        :param tree_view: TreeView to add. Must be of pyrollcall's custom treeview type
        :param title: Displays a label on the LHS of the tree view
        :return: The reference to the tree view we just created
        """
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        row.add(box)

        label = Gtk.Label(title)

        box.pack_start(label, True, True, 0)
        box.pack_start(tree_view, True, True, 0)
        self.listbox.add(row)
        self.show_all()
        return tree_view



class TreeView(Gtk.TreeView):
    """ Wraps the TreeStore inside and takes care of user selection """
    def __init__(self, list_store, column_titles: list, selection_mode=Gtk.SelectionMode.SINGLE):
        Gtk.TreeView.__init__(self, list_store)
        self.list_store = list_store
        self.column_titles = column_titles
        self.selected_items = [] # Primary keys

        # Populate TreeView rows.
        for i, title in enumerate(column_titles):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(title, renderer, text=i)
            column.set_sort_column_id(i)
            self.append_column(column)

        # Handle row selection.
        selection = self.get_selection()
        selection.set_mode(selection_mode)
        selection.connect("changed", self.on_selection_changed)

    def on_selection_changed(self, selection):
        """ The event handler on selection changed """
        self.selected_items.clear()

        model, rows = selection.get_selected_rows()
        for row in rows:
            tree_iter = model.get_iter(row)
            primary_key = model.get_value(tree_iter, 0)
            self.selected_items.append(primary_key)

    def get_selected_items(self):
        return self.selected_items

    def bind(self, objects: list):
        """ Bind this tree view with a list of objects, e.g., all students in db
        Then all fields of these objects will be displayed in the tree view.
        However, if the data gets updated, we'll need to call this method again. (bad design)
        """
        if objects is None:
            return

        self.list_store.clear()
        for o in objects:
            obj_fields = []
            for i, (key, value) in enumerate(vars(o).items()):
                if i >= len(self.column_titles):
                    break
                obj_fields.append(value)
            self.list_store.append(obj_fields)
