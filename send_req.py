import time
import requests
import json
configuration = {
  "OPENDATACAM_VERSION": "2.1.0",
  "PATH_TO_YOLO_DARKNET" : "/darknet",
  "VIDEO_INPUT": "file",
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
def send_req():
  while True:
    time.sleep(2)
    r = requests.get('http://localhost:8080/recording/5e0dc892b3b6ac003326b572')
    jsn = json.loads(r.text)
    jsn = jsn["counterSummary"]
    for name in jsn:
        if(name == "car"):
           print(jsn[name])
    print(jsn)

