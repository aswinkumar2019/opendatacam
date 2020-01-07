import time
import requests
import json
while True:
    time.sleep(2)
    r = requests.get('http://localhost:8080/recording/5e0dc892b3b6ac003326b572')
    jsn = json.loads(r.text)
    jsn = jsn["counterSummary"]["5e0dc892b3b6ac003326b572"]
    print(jsn)

