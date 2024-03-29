import matplotlib.pyplot as plt
import dict_digger
import time
import json
import requests
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
configuration = {
  "OPENDATACAM_VERSION": "2.1.0",
  "PATH_TO_YOLO_DARKNET" : "/darknet",
  "VIDEO_INPUT": "usbcam",
  "NEURAL_NETWORK": "yolov3",
  "VIDEO_INPUTS_PARAMS": {
    "file": "opendatacam_videos/night_test.mp4",
    "usbcam": "v4l2src device=/dev/video1 ! video/x-raw, framerate=30/1, width=640, height=360 ! videoconvert ! appsink",
    "usbcam_no_gstreamer": "-c 0",
    "experimental_raspberrycam_docker": "v4l2src device=/dev/video2 ! video/x-raw, framerate=30/1, width=640, height=360 ! videoconvert ! appsink",
    "raspberrycam_no_docker": "nvarguscamerasrc ! video/x-raw(memory:NVMM),width=1280, height=720, framerate=30/1, format=NV12 ! nvvidconv ! video/x-raw, format=BGRx, width=640, height=360 ! videoconvert ! video/x-raw, format=BGR ! appsink",
    "remote_cam": "YOUR IP CAM STREAM (can be .m3u8, MJPEG ...), anything supported by opencv"
  },
  "VALID_CLASSES": ["*"],
  "DISPLAY_CLASSES": [
    { "class": "bicycle", "icon": "1F6B2.svg"},
    { "class": "person", "icon": "1F6B6.svg"},
    { "class": "truck", "icon": "1F69B.svg"},
    { "class": "motorbike", "icon": "1F6F5.svg"},
    { "class": "car", "icon": "1F697.svg"},
    { "class": "bus", "icon": "1F68C.svg"}
  ],
  "PATHFINDER_COLORS": [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf"
  ],
  "COUNTER_COLORS": {
    "yellow": "#FFE700",
    "turquoise": "#A3FFF4",
    "green": "#a0f17f",
    "purple": "#d070f0",
    "red": "#AB4435"
  },
  "NEURAL_NETWORK_PARAMS": {
    "yolov3": {
      "data": "cfg/coco.data",
      "cfg": "cfg/yolov3.cfg",
      "weights": "yolov3.weights"
    },
    "yolov3-tiny": {
      "data": "cfg/coco.data",
      "cfg": "cfg/yolov3-tiny.cfg",
      "weights": "yolov3-tiny.weights"
    },
    "yolov2-voc": {
      "data": "cfg/voc.data",
      "cfg": "cfg/yolo-voc.cfg",
      "weights": "yolo-voc.weights"
    }
  },
  "TRACKER_ACCURACY_DISPLAY": {
    "nbFrameBuffer": 300,
    "settings": {
      "radius": 3.1,
      "blur": 6.2,
      "step": 0.1,
      "gradient": {
        "0.4":"orange",
        "1":"red"
      },
      "canvasResolutionFactor": 0.1
    }
  },
  "MONGODB_URL": "mongodb://127.0.0.1:27017"
}

class AnalyseWindow(Gtk.Window):

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
 
        button = Gtk.Button.new_with_label("Restore configuration")
        button.connect("clicked", self.restore_config)
        vbox.pack_start(button, False, True, 0)


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


    def analyse(self, item_name, y):
        count = [0] * 672
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
             #else:
             #   car_count[y] = jsn["counterSummary"][counter_area]["car"]-car_count[y-1]
            # y = y+1
        print("Car count this hour ",count)
        return count

    def hour_analysis(self, combo):
        r = requests.get('http://localhost:8080/recording/start')
        self.truck_count = [0] * 672
        self.person_count = [0] * 672
        self.car_count = [0] * 672
        self.bus_count = [0] * 672
        bike_count = [0] * 672
        z = 0
        self.hour_truck_count = []
        self.hour_person_count = []
        self.hour_bus_count = []
        self.hour_car_count = []
        self.hour_bicycle_count = [] 
        while True: 
            time.sleep(2)
            if z is not 0:
               plt.close()
            self.truck_count = self.analyse("truck", z)
            self.person_count = self.analyse("chair", z)
            self.car_count = self.analyse("car", z)
            self.bus_count = self.analyse("bus", z)
            self.bike_count = self.analyse("bike", z)
            self.bicycle_count = self.analyse("bicycle", z)
          #  print("Bicycle count this hour : ", self.bicycle_count)
           # print("Person count this hour : ", self.truck_count)
          #  print("Chair count this hour : ", self.person_count)

           #          Hour-wise Mobility Indicator Graph                #
            self.hour_truck_count[0:z+1] = self.truck_count[0:z+1] 
            self.hour_person_count[0:z+1] = self.person_count[0:z+1] 
            self.hour_bus_count[0:z+1] = self.bus_count[0:z+1] 
            self.hour_car_count[0:z+1] = self.car_count[0:z+1] 
            self.hour_bicycle_count[0:z+1] = self.bicycle_count[0:z+1]
            z = z + 1 
            plt.bar(self.hour_truck_count, self.hour_person_count, self.hour_bus_count, self.hour_bicycle_count, align='center', alpha=0.5)
            plt.xlabel("Vehicle Name")
            plt.ylabel("Vehicle count")
            plt.title("Mobility Indicator")
            plt.show(block = False)
            print("Bicycle count this hour : ", self.hour_bicycle_count)
            print("Chair count this hour : ", self.hour_person_count)

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
 
    def restore_config(self, button):
        restore_file = open("./config.json", "w")
        restore_file.write(json.dumps(configuration))

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

window = AnalyseWindow()        
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
