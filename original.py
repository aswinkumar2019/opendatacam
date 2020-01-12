import dict_digger
import time
from send_req import configuration
import json
import requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class LabelWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Youcode Intelligence Solutions")
        vbox_last = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_last.set_homogeneous(False)
        hbox_last = Gtk.Box(spacing=10)
        hbox_last.set_homogeneous(False)
        hbox_top = Gtk.Box(spacing=10)
        hbox_top.set_homogeneous(False)
        hbox_analysis = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        hbox_analysis.set_homogeneous(False)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_homogeneous(False)
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        hbox.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_right.set_homogeneous(False)
        hbox_top.pack_start(hbox_analysis, False, True, 10)
        hbox_top.pack_start(vbox, False, True, 10)
        hbox_top.pack_start(hbox, False, True, 10)
        hbox_top.pack_start(vbox_right, False, True, 10)
        vbox_last.pack_start(hbox_top, False, True, 10)
        vbox_last.pack_end(hbox_last, False, True, 300)
        button = Gtk.Button.new_with_label("Start hourly analysis")
        button.connect("clicked", self.hour_analysis)
        hbox_analysis.pack_start(button, False, True, 10)

        
        self.label3 = Gtk.Label("Choose the model")
        vbox.pack_start(self.label3, False, True, 20)

        avail_models = ["Choose Model", "Yolo V3", "Yolo V2", "Yolo V3(tiny)"]
        model_combo = Gtk.ComboBoxText()
        model_combo.connect("changed", self.on_model_combo_changed)
        for models in avail_models:
            model_combo.append_text(models)

        vbox.pack_start(model_combo, False, True, 0)
        
        self.label4 = Gtk.Label("Choose the video input type")
        vbox.pack_start(self.label4, False, True, 20)

        
        video_input = ["file", "usbcam"]
        video_combo = Gtk.ComboBoxText()
        video_combo.connect("changed", self.on_video_combo_changed)
        for type in video_input:
            video_combo.append_text(type)

        vbox.pack_start(video_combo, False, True, 0)


        button = Gtk.Button.new_with_label("Start")
        button.connect("clicked", self.run)
        vbox.pack_start(button, False, True, 0)

       
        button = Gtk.Button.new_with_mnemonic("_Record")
        button.connect("clicked", self.record_start)
        hbox.pack_start(button, False, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Stop Recording")
        button.connect("clicked", self.record_stop)
        hbox.pack_start(button, False, True, 0)
        
        self.entry = Gtk.Entry()
        self.entry.set_text("Enter recording id")
        hbox.pack_start(self.entry, False, True, 0)
         
        button = Gtk.Button.new_with_mnemonic("Get counter for Recording")
        button.connect("clicked", self.record_counter)
        hbox.pack_start(button, False, True, 0)
   
        self.label2 = Gtk.Label("Press Get counter for recording to get counter for a recording")
        hbox.pack_start(self.label2, False, True, 0)

 
        button = Gtk.Button.new_with_mnemonic("_Get Recording id")
        button.connect("clicked", self.get_id)
        vbox_right.pack_start(button, False, True, 0)

        self.label1 = Gtk.Label("Press Get Recording id to get list of old recordings")
        vbox_right.pack_start(self.label1, False, True, 100)

        button = Gtk.Button.new_with_mnemonic("_Recording status")
        button.connect("clicked", self.record_status)
        vbox_right.pack_start(button, False, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Get Counter line")
        button.connect("clicked", self.counter_areas)
        vbox_right.pack_start(button, False, True, 0)
        
        self.label_eco = Gtk.Label("Press Get counter for recording to get counter for a recording")
        hbox_last.pack_start(self.label_eco, False, True, 50)

        self.label_mobi = Gtk.Label("Press Get counter for recording to get counter for a recording")
        hbox_last.pack_start(self.label_mobi, False, True, 50)

        self.add(vbox_last)


    def analyse(self, item_name):
        count = [0] * 672
        y = 0
        area_assign = 0
        counter_area = 0
        sub_value = 0
        r = requests.get('http://localhost:8080/status')
   #    r = requests.get('http://localhost:8080/counter/areas')
        jsn = json.loads(r.text)
        counter_summary = jsn["counterSummary"].items()
        if(area_assign == 0):
            while(counter_area == 0):
                print("waiting for first vehicle to pass")
                for key,value in jsn["counterSummary"].items():
                   counter_area = key
        area_assign = 1
        if(y is  0):
                if(dict_digger.dig(jsn,"counterSummary",counter_area,item_name) == None):
                   sub_value = 0
                   count[y] = 0
                else:
                   sub_value = jsn["counterSummary"][counter_area][item_name]
                   count[y] = jsn["counterSummary"][counter_area][item_name]
        else:
                for x in range(1,y-1):
                  sub_value = sub_value + count[x]
                if(dict_digger.dig(jsn,"counterSummary",counter_area,item_name) == None):
                  count[y] = 0
                else:
                  count[y] = jsn["counterSummary"][counter_area][item_name] - sub_value        
        print("Truck count this hour is ",count[y])
        print(sub_value)
        y = y+1
             #else:
             #   car_count[y] = jsn["counterSummary"][counter_area]["car"]-car_count[y-1]
            # y = y+1
        print("Car count this hour ",count)
        return count

    def hour_analysis(self, combo):
        r = requests.get('http://localhost:8080/recording/start')
        truck_count = [0] * 672
        person_count = [0] * 672
        car_count = [0] * 672
        bus_count = [0] * 672
        bike_count = [0] * 672 
        while True: 
            time.sleep(5)
            self.truck_count = self.analyse("truck")
            self.person_count = self.analyse("chair")
            self.car_count = self.analyse("car")
            self.bus_count = self.analyse("bus")
            self.bike_count = self.analyse("bike")
            self.bicycle_count = self.analyse("bicycle")
            print("Bicycle count this hour : ", self.bicycle_count)
           # print("Person count this hour : ", self.truck_count)
            print("Chair count this hour : ", self.person_count)
           # print("Person count this hour : ", self.car_count)
           # print("Person count this hour : ", self.bus_count)
           # print("Person count this hour : ", self.bike_count)

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
          self.counter_area = key
        display = "Counter area is " + str(self.counter_area)
        if(dict_digger.dig(jsn, "counterSummary", self.counter_area, "car") == None):
           car_count = 0
        else:
           car_count = jsn["counterSummary"][self.counter_area]["car"]
        display = display + "\nCar count is " + str(car_count)
        if(dict_digger.dig(jsn, "counterSummary", self.counter_area, "truck") == None):
           truck_count = 0
        else:
           truck_count = jsn["counterSummary"][self.counter_area]["truck"]
        display = display + "\nTruck count is " + str(truck_count)
        if(dict_digger.dig(jsn, "counterSummary", self.counter_area, "bus") == None):
           bus_count = 0
        else:
           bus_count = jsn["counterSummary"][self.counter_area]["bus"]
        display = display + "\nBus count is " + str(bus_count)
        if(dict_digger.dig(jsn, "counterSummary", self.counter_area, "person") == None):
           person_count = 0
        else:
           person_count = jsn["counterSummary"][self.counter_area]["person"]
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
