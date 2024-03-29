import requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class LabelWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Youcode Intelligence Solutions")
        self.set_border_width(10)
        hbox_top = Gtk.Box(spacing=10)
        hbox_top.set_homogeneous(False)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        hbox.set_homogeneous(False)

        hbox_top.pack_start(vbox, True, True, 0)
        hbox_top.pack_start(hbox, True, True, 0)

        avail_models = ["Yolo V3", "Yolo V2", "Yolo V3(tiny)"]
        model_combo = Gtk.ComboBoxText()
        model_combo.connect("changed", self.on_model_combo_changed)
        for models in avail_models:
            model_combo.append_text(models)

        vbox.pack_start(model_combo, False, False, 0)

        

        button = Gtk.Button.new_with_mnemonic("Start")
        button.connect("clicked", self.run)
        vbox.pack_start(button, True, True, 0)
        

        button = Gtk.Button.new_with_mnemonic("_Record")
        button.connect("clicked", self.record_start)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Stop Recording")
        button.connect("clicked", self.record_stop)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Recording status")
        button.connect("clicked", self.record_status)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Get Counter line")
        button.connect("clicked", self.counter_areas)
        hbox.pack_start(button, True, True, 0)
        self.add(hbox_top)
        
    def on_model_combo_changed(self, combo):
        text = combo.get_active_text()
        if text is not None:
            print("Selected: currency=%s" % text)


    def run(self, button):
        r = requests.get('http://localhost:8080/start')
        print("Starting,verify the status before starting recording")
        print(r)

    def record_start(self, button):
        r = requests.get('http://localhost:8080/recording/start')
        print(r)
    def record_stop(self, button):
        r = requests.get('http://localhost:8080/recording/stop')
        print(r)

    def record_status(self, button):
        r = requests.get('http://localhost:8080/recordings?offset=:offset&limit=:limit')
        print(r.json())

    def counter_areas(self, button):
        r = requests.get('http://localhost:8080/counter/areas')
        print(r.json())


win = LabelWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

