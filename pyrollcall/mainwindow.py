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

from pyrollcall.widget import ConfirmDialog
from pyrollcall.widget import FormDialog
from pyrollcall.widget import TreeView


class DataType(IntEnum):
    COURSE = 0
    STUDENT = 1


class MainWindow(Gtk.Window):
    """ The main window of pyrollcall """
    def __init__(self):
        Gtk.Window.__init__(self, title="pyrollcall")
        self.set_wmclass("pyrollcall", "pyRollCall")
        self.set_default_geometry(640, 480)
        self.set_border_width(10)

        self.database = None
        self.session = None

        self.start_rollcall_btn = Gtk.Button("Start")
        self.end_rollcall_btn = Gtk.Button("End")
        self.rollcall_take_photo_btn = Gtk.Button("Take Photo")
        self.rollcall_choose_photo_btn = Gtk.Button("Choose Photo")
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

        self.rollcall_take_photo_btn.connect("clicked", self.rollcall_take_photo)
        self.rollcall_take_photo_btn.set_sensitive(False)

        self.rollcall_choose_photo_btn.connect("clicked", self.rollcall_choose_photo)
        self.rollcall_choose_photo_btn.set_sensitive(False)

        header_box.pack_start(self.start_rollcall_btn, True, True, 0)
        header_box.pack_start(self.end_rollcall_btn, True, True, 0)
        header_box.pack_start(self.rollcall_take_photo_btn, True, True, 0)
        header_box.pack_start(self.rollcall_choose_photo_btn, True, True, 0)

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
        create_btn.connect("clicked", self.create)

        edit_btn = Gtk.Button("Edit")
        edit_btn.connect("clicked", self.edit)

        remove_btn = Gtk.Button("Remove")
        remove_btn.connect("clicked", self.remove)

        take_photos_btn = Gtk.Button("Take Photos")
        take_photos_btn.connect("clicked", self.take_photos)

        train_model_compute_all_btn = Gtk.Button("Retrain Model (slow)")
        train_model_compute_all_btn.connect("clicked", self.train_model_compute_all)

        train_model_compute_new_btn = Gtk.Button("Train Model (fast)")
        train_model_compute_new_btn.connect("clicked", self.train_model_compute_new)

        header_box.pack_start(create_btn, True, True, 0)
        header_box.pack_start(edit_btn, True, True, 0)
        header_box.pack_start(remove_btn, True, True, 0)
        header_box.pack_start(take_photos_btn, True, True, 0)
        header_box.pack_start(train_model_compute_all_btn, True, True, 0)
        header_box.pack_start(train_model_compute_new_btn, True, True, 0)


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
        self.courses_tree_view = TreeView(Gtk.ListStore(int, str, str, int), ["id", "semester", "Name", "Student Count"])
        if self.database is not None:
            self.courses_tree_view.update(self.database.courses)
        courses_box.pack_start(self.courses_tree_view, True, True, 0)

        # Students page.
        students_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        students_row = Gtk.ListBoxRow()
        students_row.add(students_box)
        students_listbox.add(students_row)
        self.students_tree_view = TreeView(Gtk.ListStore(str, str, bool), ["id", "Name", "Has Photos"])
        if self.database is not None:
            self.students_tree_view.update(self.database.students)
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
        self.courses_tree_view.update(self.database.courses)
        self.students_tree_view.update(self.database.students)


    def start_rollcall(self, widget):
        form_dialog = FormDialog(self, title="Start a Roll Call", message="Which one is your class today?")
        # Add a student tree view to the dialog.
        courses_list_store = Gtk.ListStore(int, str, str, int)
        courses_tree_view = TreeView(courses_list_store, ["ID", "Semester", "Name", "Student Count"], Gtk.SelectionMode.MULTIPLE)
        form_dialog.add_tree_view(courses_tree_view, title="Courses")
        courses_tree_view.update(self.database.courses)
        response = form_dialog.run()

        if response == Gtk.ResponseType.OK and len(courses_tree_view.get_selected_items()) > 0:
            selected_course_id = courses_tree_view.get_selected_items()[0]
            selected_course = self.database.get_course(selected_course_id)
            # Initiate a new rollcall session using the selected course.
            self.session = Session(selected_course)
            self.start_rollcall_btn.set_sensitive(False)
            self.end_rollcall_btn.set_sensitive(True)
            self.rollcall_take_photo_btn.set_sensitive(True)
            self.rollcall_choose_photo_btn.set_sensitive(True)
            self.update_session_tree_view()
            self.current_rollcall_course_label.set_text("Current roll call: " + self.session.__str__())

        form_dialog.destroy()

    def stop_rollcall(self, widget):
        confirm_dialog = ConfirmDialog(self, title="End Roll Call", message="End current roll call?")
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.session.export()
            self.session = None
            self.start_rollcall_btn.set_sensitive(True)
            self.end_rollcall_btn.set_sensitive(False)
            self.rollcall_take_photo_btn.set_sensitive(False)
            self.rollcall_choose_photo_btn.set_sensitive(False)
            self.current_rollcall_course_label.set_text("No ongoing rollcall.")

        confirm_dialog.destroy()

    def rollcall_take_photo(self, widget):
        confirm_dialog = ConfirmDialog(self, title="Roll Call", message="Perform rollcall via taking photo?")
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            img_path = face.collect_faces()[0]
            arrived_student_ids = face.recognize_faces(self.database, img_path)

            for id in arrived_student_ids:
                self.session.mark_as_arrived(id)

            self.update_session_tree_view()
            self.current_rollcall_course_label.set_text("Current roll call: " + self.session.__str__())

        confirm_dialog.destroy()

    def rollcall_choose_photo(self, widget):
        file_chooser_dialog = Gtk.FileChooserDialog("Please choose a photo", None, Gtk.FileChooserAction.OPEN,
                                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                                     Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = file_chooser_dialog.run()

        if response == Gtk.ResponseType.OK:
            img_path = file_chooser_dialog.get_filename()
            arrived_student_ids = face.recognize_faces(self.database, img_path)

            for id in arrived_student_ids:
                self.session.mark_as_arrived(id)

            self.update_session_tree_view()
            self.current_rollcall_course_label.set_text("Current roll call: " + self.session.__str__())

        file_chooser_dialog.destroy()


    def create(self, widget):
        if self.manage_page_notebook.get_current_page() == DataType.COURSE:
            self.create_course()
        elif self.manage_page_notebook.get_current_page() == DataType.STUDENT:
            self.create_student()

    def edit(self, widget):
        if self.manage_page_notebook.get_current_page() == DataType.COURSE:
            # The selection model of courses tree view is SINGLE,
            # so we'll try to get the first item in the list.
            if len(self.courses_tree_view.get_selected_items()) == 0:
                return
            selected_course_id = self.courses_tree_view.get_selected_items()[0]
            selected_course = self.database.get_course(selected_course_id)
            self.edit_course(selected_course)
        elif self.manage_page_notebook.get_current_page() == DataType.STUDENT:
            if len(self.students_tree_view.get_selected_items()) == 0:
                return
            selected_student_id = self.students_tree_view.get_selected_items()[0]
            selected_student = self.database.get_student(selected_student_id)
            self.edit_student(selected_student)

    def remove(self, widget):
        if self.manage_page_notebook.get_current_page() == DataType.COURSE:
            if len(self.courses_tree_view.get_selected_items()) == 0:
                return
            selected_course_id = self.courses_tree_view.get_selected_items()[0]
            selected_course = self.database.get_course(selected_course_id)
            self.remove_course(selected_course)
        elif self.manage_page_notebook.get_current_page() == DataType.STUDENT:
            if len(self.students_tree_view.get_selected_items()) == 0:
                return
            selected_student_id = self.students_tree_view.get_selected_items()[0]
            selected_student = self.database.get_student(selected_student_id)
            self.remove_student(selected_student)

    def take_photos(self, widget):
        selected_students_ids = self.students_tree_view.get_selected_items()

        if len(selected_students_ids) > 0:
            selected_student_id = selected_students_ids[0]
            selected_student = self.database.get_student(selected_student_id)

            form_dialog = FormDialog(self, title="Take Photos", message="Click OK and Press SPACE to take photos")
            photo_count_entry = form_dialog.add_entry("Number of Photos")
            photo_count_entry.set_text("5")
            response = form_dialog.run()

            if response == Gtk.ResponseType.OK:
                face.collect_faces(selected_student, img_count=int(photo_count_entry.get_text()))
                self.students_tree_view.update(self.database.students)

            form_dialog.destroy()

    def train_model_compute_all(self, widget):
        confirm_dialog = ConfirmDialog(self, title="Training Model", message="This may take a long time, proceed?")
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            face.encode_faces(self.database, "faces/")
            self.database.dump()

        confirm_dialog.destroy()

    def train_model_compute_new(self, widget):
        confirm_dialog = ConfirmDialog(self, title="Training Model", message="This may take a while, proceed?")
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            face.encode_new_faces(self.database, "faces/")
            self.database.dump()

        confirm_dialog.destroy()


    def create_course(self):
        form_dialog = FormDialog(self, title="Create New Course", message="Create New Course...")
        # Add semester and name entries to the dialog.
        semester_entry = form_dialog.add_entry("Semester  ")
        name_entry = form_dialog.add_entry("Class Name")
        # Add a student tree view to the dialog.
        students_list_store = Gtk.ListStore(str, str, bool)
        students_tree_view = TreeView(students_list_store, ["ID", "Name", "Has Photos"], Gtk.SelectionMode.MULTIPLE)
        form_dialog.add_tree_view(students_tree_view, title="Students")
        students_tree_view.update(self.database.students)

        response = form_dialog.run()

        if response == Gtk.ResponseType.OK:
            c = self.database.add_course(semester_entry.get_text(), name_entry.get_text())
            selected_items = students_tree_view.get_selected_items()
            for student_id in selected_items:
                s = self.database.get_student(student_id)
                c.add_student(s)
            self.courses_tree_view.update(self.database.courses)
            self.database.dump()

        form_dialog.destroy()

    def edit_course(self, course: Course):
        form_dialog = FormDialog(self, title="Edit Course", message="Edit Course...")
        # Add semester and name entries to the dialog.
        semester_entry = form_dialog.add_entry("Semester  ")
        name_entry = form_dialog.add_entry("Class Name")
        semester_entry.set_text(course.semester)
        name_entry.set_text(course.name)

        # Add a student tree view to the dialog.
        students_list_store = Gtk.ListStore(str, str, bool)
        students_tree_view = TreeView(students_list_store, ["ID", "Name", "Has Photos"], Gtk.SelectionMode.MULTIPLE)
        form_dialog.add_tree_view(students_tree_view, title="Students")
        students_tree_view.update(self.database.students)

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
            course.semester = semester_entry.get_text()
            course.name = name_entry.get_text()
            selected_items = students_tree_view.get_selected_items()

            course.students.clear()
            for student_id in selected_items:
                s = self.database.get_student(student_id)
                course.add_student(s)
            self.courses_tree_view.update(self.database.courses)
            self.database.dump()

        form_dialog.destroy()

    def remove_course(self, course: Course):
        confirm_dialog = ConfirmDialog(self, title="Remove Course", message="Remove {} {}?".format(
            course.semester, course.name))
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.database.remove_course(course)
            self.courses_tree_view.update(self.database.courses)
            self.database.dump()

        confirm_dialog.destroy()



    def create_student(self):
        form_dialog = FormDialog(self, title="Create New Student", message="Create New Student...")
        id_entry = form_dialog.add_entry("Student ID  ")
        name_entry = form_dialog.add_entry("Student Name")
        response = form_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.database.add_student(id_entry.get_text(), name_entry.get_text())
            self.students_tree_view.update(self.database.students)
            self.database.dump()

        form_dialog.destroy()

    def edit_student(self, student: Student):
        form_dialog = FormDialog(self, title="Edit Student", message="Edit Student...")
        id_entry = form_dialog.add_entry("Student ID  ")
        name_entry = form_dialog.add_entry("Student Name")
        id_entry.set_sensitive(False)
        id_entry.set_text(student.id)
        name_entry.set_text(student.name)
        response = form_dialog.run()

        if response == Gtk.ResponseType.OK:
            student.id = id_entry.get_text()
            student.name = name_entry.get_text()
            self.students_tree_view.update(self.database.students)
            self.database.dump()

        form_dialog.destroy()

    def remove_student(self, student: Student):
        confirm_dialog = ConfirmDialog(self, title="Remove Student", message="Remove {} {}?".format(
            student.id, student.name))
        response = confirm_dialog.run()

        if response == Gtk.ResponseType.OK:
            self.database.remove_student(student)
            self.students_tree_view.update(self.database.students)
            self.database.dump()

        confirm_dialog.destroy()


    def show(self):
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        Gtk.main()
