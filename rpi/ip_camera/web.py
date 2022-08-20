import time
import threading

import numpy as np
import cv2
import imutils

import ip_camera_module

from flask import Response
from flask import Flask
from flask import render_template

app = Flask(__name__)

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")


@app.route("/video_feed")
def video_feed():
  return Response(generate(),
                    mimetype = "multipart/x-mixed-replace; boundary=frame")

def generate():
  while True:
    img = cap.get_img()
    if img is None:
      time.sleep(0.1)
      continue
    (flag, encodedImage) = cv2.imencode(".jpg", img)
    if not flag:
      time.sleep(0.1)
      continue
    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(encodedImage) + b'\r\n')


def camera_watch():
  global lock, img_s
  cap = ip_camera_module.IPCamera(src="rtsp://admin:p9048480795@192.168.0.200:554/cam/realmonitor?channel=1&subtype=0",
                 debug=True)
  cap.start()
  
  while True:
    t = time.time()
    
    frame = cap.get_img()

    if frame is None:
        time.sleep(0.1)
        continue
    
    with lock:
      if img_s is None:
        img_s = frame.copy()
    #print(1 / (time.time() - t))


img_s = None
lock = threading.Lock()

##tr1 = threading.Thread(target=camera_watch, args=())
##tr1.start()

cap = ip_camera_module.IPCamera(src="rtsp://admin:p9048480795@192.168.0.200:554/cam/realmonitor?channel=1&subtype=0",
                 debug=True)
cap.start()

app.run(host="0.0.0.0", port=8000, debug=False,
        threaded=True, use_reloader=False)
