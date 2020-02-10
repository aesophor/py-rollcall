# -*- encoding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ConfirmDialog(Gtk.Dialog):
    """ Ask user to confirm the specified message """
    def __init__(self, parent, title="", message="", width=150, height=50):
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
    def __init__(self, parent, title="", message="", width=150, height=50):
        ConfirmDialog.__init__(self, parent, title=title, message=message,
            width=width, height=height)

        self.listbox = Gtk.ListBox(margin=5)
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.get_content_area().add(self.listbox)
        self.show_all()

    def add_entry(self, title="", text="", spacing=100):
        """ An entry in Gtk is like a text input area
        :param title: Displays a label on the LHS of the entry
        :param text: The default text in the entry
        :return: The reference to the entry we just created
        """
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=spacing)
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

    def update(self, objects: list):
        """ Update the content of tree view with a list of objects, e.g., all students in db.
        Then all fields of these objects will be displayed in the tree view.
        """
        if objects is None:
            return

        self.list_store.clear()
        for o in objects:
            obj_fields = []
            for i, (key, value) in enumerate(o.dict.items()):
                if i >= len(self.column_titles):
                    break
                obj_fields.append(value)
            self.list_store.append(obj_fields)
