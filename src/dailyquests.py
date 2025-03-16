import gi
import database
import time

gi.require_version("Gtk", "3.0")
gi.require_version("XApp", "1.0")
from gi.repository import Gtk, XApp

DATE_FORMAT = "%d/%m/%Y"
DAY_IN_SECONDS = 60 * 60 * 24

class DailyQuestsApp(Gtk.Application):
    def __init__(self):
        super().__init__()

        builder = Gtk.Builder()
        builder.add_from_file("questapp.glade")
        builder.connect_signals(self)

        self.list_box = builder.get_object("list_box")
        
        self.db = database.TasksDatabase()

        self.current_date = self.getCurrentDateAsSeconds()
        self.date = self.current_date

        self.date_label = builder.get_object("date_label")
        self.updateDateLabel()

        self.db.moveIncompleteTasks(self.date)

        self.loadListByDate()
        
        self.win = builder.get_object("quest_window")
        self.win.show_all()

        return

    def getCurrentDateAsSeconds(self):
        date = time.mktime(time.strptime(time.strftime("%d/%m/%Y", time.localtime()), "%d/%m/%Y"))
        return date

    def updateDateLabel(self):
        self.date_label.set_label(time.strftime(DATE_FORMAT, time.localtime(self.date)))
        return

    def loadListByDate(self):
        for row in self.list_box.get_children():
            self.list_box.remove(row)
        tasks = self.db.tasksByDate(self.date)
        for row in tasks:
            taskid = int(row[0])
            task = row[1]
            status = bool(row[2])
            list_item = ListItem(taskid, task, status)
            list_item.getCheckButton().connect("toggled", self.updateTask, taskid)
            self.list_box.add(list_item)
        self.list_box.show_all()
        return

    def incrementDate(self, button):
        self.date += DAY_IN_SECONDS
        self.updateDateLabel()
        self.loadListByDate()
        return

    def decrementDate(self, button):
        self.date -= DAY_IN_SECONDS
        self.updateDateLabel()
        self.loadListByDate()
        return


    def onDestroy(self, *args):
        Gtk.main_quit()
        return

    def addTask(self, entry):
        input = entry.get_text()
        if (input != ""):
            taskid = len(self.list_box)
            list_item = ListItem(taskid, input, False)
            list_item.getCheckButton().connect("toggled", self.updateTask, taskid)
            self.list_box.add(list_item)
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
    
    def updateTask(self, button, taskid):
        self.db.updateTask(taskid, self.date, button.get_active())
        return

    def taskKeyPress(self, widget, event):
        return

class ListItem(Gtk.ListBoxRow):
    def __init__(self, taskid: int, task: str, state: bool):
        self.taskid = taskid
        super().__init__()
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        hor_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.check_button = Gtk.CheckButton();
        self.check_button.set_active(state)
        hor_box.add(self.check_button)

        hor_box.add(Gtk.Label(label=task))
        box.add(hor_box)

        self.add(box)
        return
    
    def getTaskId(self) -> int:
        return self.taskid

    def getCheckButton(self) -> Gtk.CheckButton:
        return self.check_button
    
app = DailyQuestsApp()
Gtk.main()
