import gi
import database
import time

gi.require_version("Gtk", "3.0")
gi.require_version("XApp", "1.0")
from gi.repository import Gtk, XApp

class DailyQuestsApp(Gtk.Application):
    def __init__(self):
        super().__init__()

        builder = Gtk.Builder()
        builder.add_from_file("questapp.glade")
        builder.connect_signals(self)

        self.list_box = builder.get_object("list_box")
        self.task_input_entry = builder.get_object("task_input_entry")
        
        self.db = database.TasksDatabase()

        self.date = time.strftime("%d/%m/%Y", time.localtime())
        self.date_label = builder.get_object("date_label")
        self.date_label.set_label(self.date)

        self.loadListByDate(self.date)
        
        self.win = builder.get_object("quest_window")
        self.win.show_all()

        self.status = XApp.StatusIcon()
        self.status.connect("activate", self.onClickStatusIcon)
        return

    def loadListByDate(self, date):
        for row in self.list_box.get_children():
            self.list_box.remove(row)
        tasks = self.db.tasksByDate(date)
        for row in tasks:
            self.list_box.add(ListItem(int(row[0]), row[1], bool(row[2])))
        self.list_box.show_all()
        return

    def incrementDate(self, button):
        new_date = time.mktime(time.strptime(self.date, "%d/%m/%Y")) + (60 * 60 * 24)
        self.date = time.strftime("%d/%m/%Y", time.localtime(new_date))
        self.date_label.set_label(self.date)
        self.loadListByDate(self.date)
        return

    def decrementDate(self, button):
        new_date = time.mktime(time.strptime(self.date, "%d/%m/%Y")) - (60 * 60 * 24)
        self.date = time.strftime("%d/%m/%Y", time.localtime(new_date))
        self.date_label.set_label(self.date)
        self.loadListByDate(self.date)
        return

    def onClickStatusIcon(self, button, time, data):
        self.win.show_all()
        return

    def onDestroy(self, *args):
        Gtk.main_quit()
        return

    def addTask(self, entry):
        input = entry.get_text()
        if (input != ""):
            taskid = len(self.list_box) - 1
            self.list_box.add(ListItem(taskid, input, False))
            self.list_box.show_all()
            self.db.insertTask(taskid, self.date, input)
        entry.set_text("")
        return

    def removeTask(self, button):
        remove = self.list_box.get_selected_row()
        self.db.deleteTask(remove.getTaskId(), self.date)
        self.list_box.remove(remove)
        self.list_box.show_all()
        return

    def taskKeyPress(self, widget, event):
        #print(widget, event)
        return

class ListItem(Gtk.ListBoxRow):
    def __init__(self, taskid, task, state):
        self.taskid = taskid
        super().__init__()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        hor_box.add(Gtk.CheckButton())
        hor_box.add(Gtk.Label(label=task))
        box.add(hor_box)

        self.add(box)
        return
    
    def getTaskId(self):
        return self.taskid

app = DailyQuestsApp()
Gtk.main()
