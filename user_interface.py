import gi

gi.require_version("Gtk", "3.0")
gi.require_version("XApp", "1.0")
from gi.repository import Gtk, XApp

class Handler():
    def __init__(self, builder):
        self.list_box = builder.get_object("list_box")
        self.task_input_entry = builder.get_object("task_input_entry")
        return

    def onDestroy(self, *args):
        Gtk.main_quit()
        return

    def addTask(self, button):
        input = self.task_input_entry.get_text()
        if (input != ""):
            self.list_box.add(ListItem(input))
            self.list_box.show_all()
        self.task_input_entry.set_text("")
        return

    def removeTask(self, button):
        remove = self.list_box.get_selected_row()
        self.list_box.remove(remove)
        self.list_box.show_all()
        return

    def taskKeyPress(self, widget, event):
        print(widget, event)
        return

class ListItem(Gtk.ListBoxRow):
    def __init__(self, task):
        super().__init__()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        #separator_top = Gtk.Separator(margin_bottom=4)
        #box.add(separator_top)
        
        hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        hor_box.add(Gtk.CheckButton())
        hor_box.add(Gtk.Label(task))
        box.add(hor_box)

        #separator_bottom = Gtk.Separator(margin_top=4)
        #box.add(separator_bottom)

        self.add(box)
        return

def run_user_interface():
    builder = Gtk.Builder()
    builder.add_from_file("questapp.glade")
    builder.connect_signals(Handler(builder))
    app = builder.get_object("quest_app")
    app.show_all()
    Gtk.main()
    return
