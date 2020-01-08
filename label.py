from send_req import configuration
import json
import requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class LabelWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Youcode Intelligence Solutions")
        
        hbox_top = Gtk.Box(spacing=10)
        hbox_top.set_homogeneous(False)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        hbox.set_homogeneous(False)
        
        hbox_top.pack_start(vbox, True, True, 0)
        hbox_top.pack_start(hbox, True, True, 0)
        
        avail_models = ["Choose Model", "Yolo V3", "Yolo V2", "Yolo V3(tiny)"]
        model_combo = Gtk.ComboBoxText()
        model_combo.connect("changed", self.on_model_combo_changed)
        for models in avail_models:
            model_combo.append_text(models)

        vbox.pack_start(model_combo, True, True, 0)
 
        video_input = ["file", "usbcam"]
        video_combo = Gtk.ComboBoxText()
        video_combo.connect("changed", self.on_video_combo_changed)
        for type in video_input:
            video_combo.append_text(type)

        vbox.pack_start(video_combo, True, True, 0)


        button = Gtk.Button.new_with_label("Start")
        button.connect("clicked", self.run)
        vbox.pack_start(button, True, True, 0)

       
        button = Gtk.Button.new_with_mnemonic("_Record")
        button.connect("clicked", self.record_start)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Stop Recording")
        button.connect("clicked", self.record_stop)
        hbox.pack_start(button, True, True, 0)
        
        self.entry = Gtk.Entry()
        self.entry.set_text("Enter recording id")
        hbox.pack_start(self.entry, True, True, 0)
         
        button = Gtk.Button.new_with_mnemonic("Get counter for Recording")
        button.connect("clicked", self.record_counter)
        hbox.pack_start(button, True, True, 0)
   
        self.label2 = Gtk.Label("Press Get counter for recording to get counter for a recording")
        hbox.pack_start(self.label2, True, True, 0)

 
        button = Gtk.Button.new_with_mnemonic("_Get Recording id")
        button.connect("clicked", self.get_id)
        hbox.pack_start(button, True, True, 0)

        self.label1 = Gtk.Label("Press Get Recording id to get list of old recordings")
        hbox.pack_start(self.label1, True, True, 0)

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
            print("Selected: model=%s" % text)
        write_file = open("./config.json", "w")
        json_value = json.dumps(configuration)
        json_content = json.loads(json_value)
        json_content["NEURAL_NETWORK"] = text
        modified_value = json.dumps(json_content)
        write_file.write(modified_value)

    def on_video_combo_changed(self, combo):
        text = combo.get_active_text()
        if text is not None:
            print("Selected: input=%s" % text)
        write_file = open("./config.json", "w")
        json_value = json.dumps(configuration)
        json_content = json.loads(json_value)
        json_content["VIDEO_INPUT"] = text
        modified_value = json.dumps(json_content)
        write_file.write(modified_value)


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

    def record_counter(self, button):
        print(self.entry.get_text())
        areas = self.entry.get_text()
        link = 'http://localhost:8080/recording/' + str(areas) + '/counter'
        r = requests.get(link)
        jsn = json.loads(r.text)
        for key,value in jsn["counterSummary"].items():
          counter_area = key
        display = "Counter area is " + str(counter_area)
        car_count = jsn["counterSummary"][counter_area]["car"]
        display = display + "\nCar count is " + str(car_count)
        truck_count = jsn["counterSummary"][counter_area]["truck"]
        display = display + "\nTruck count is " + str(truck_count)
        bus_count = jsn["counterSummary"][counter_area]["bus"]
        display = display + "\nBus count is " + str(bus_count)
        person_count = jsn["counterSummary"][counter_area]["person"]
        display = display + "\nPerson count is " + str(person_count)
        self.label2.set_text(display)

   
    def get_id(self, button):
        r = requests.get('http://localhost:8080/recordings?offset=:offset&limit=:limit')
        jsn = json.loads(r.text)
        out = " "
        for count in range(0,len(jsn["recordings"])):
            out = out + "\n" + jsn["recordings"][count]["_id"]
            print (out)
        self.label1.set_text(out)



    def record_status(self, button):
        r = requests.get('http://localhost:8080/status')
        print(r.json())

    def counter_areas(self, button):
        r = requests.get('http://localhost:8080/counter/areas')
        print(r.json())
        print(configuration)

window = LabelWindow()        
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
