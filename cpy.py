import requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#start
#r = requests.get('http://localhost:8080/start')

#print (r)
#print (r.json())

#start recording

#r = requests.get('http://localhost:8080/recording/start')

#stop recording

#r = requests.get('http://localhost:8080/recording/stop')

#check status

#r = requests.get('http://localhost:8080/recording/status')


#Get recording status

#r = requests.get('http://localhost:8080/recordings?offset=:offset&limit=:limit')


class ButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Youcode Intelligence Solutions")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button = Gtk.Button.new_with_label("Start")
        button.connect("clicked", self.run)
        hbox.pack_start(button, True, True, 0)

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


win = ButtonWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
