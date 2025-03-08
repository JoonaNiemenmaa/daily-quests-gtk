import gi

gi.require_version("Gtk", "3.0")
gi.require_version("XApp", "1.0")
from gi.repository import Gtk, XApp

class TodoWindow(Gtk.Window):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        return

class TodoStatusIcon(XApp.StatusIcon):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.connect("activate", self.on_click)
        self.win = MainWindow()
        return
    
    def on_click(self, icon, button, time):
        MOUSE_BUTTON_LEFT = 1;
        MOUSE_BUTTON_MIDDLE = 2;
        MOUSE_BUTTON_RIGHT = 3;

        if (button == MOUSE_BUTTON_LEFT):
            self.win.show_all()
        return

def run_user_interface():
    status = TodoStatusIcon()
    Gtk.main()
    return
