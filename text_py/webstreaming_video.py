import os
import sys
import threading
import argparse
import time
import math

import numpy as np
import cv2
import imutils
from pytesseract import Output
import pytesseract

from flask import Response
from flask import Flask
from flask import render_template

codec = cv2.VideoWriter_fourcc('M','J','P','G')
lock = threading.Lock()

def recognition(img):
  rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  results = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang="rus")

  for i in range(len(results["text"])):
    x = results["left"][i]
    y = results["top"][i]
    w = results["width"][i]
    h = results["height"][i]

    text = results["text"][i]
    conf = int(float(results["conf"][i]))

    if conf > 5:

      print("Confidence: {}".format(conf))
      print("Text: {}".format(text))
      print("")

      text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
      cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                  1.2, (0, 0, 255), 3)
  return img

class WebcamVideoStream:
    def __init__(self, src=0):
        print('Camera %s init...' % src)
        self.src = src
        self.cap = cv2.VideoCapture(self.src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FOURCC, codec)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)           
        (self.grabbed, self.frame) = self.cap.read()
        self.started = False
        self.read_lock = threading.Lock()

    def set(self, var1, var2):
        self.cap.set(var1, var2)

    def get(self, var1):
        self.cap.get(var1)
        
    def start(self):
        if self.started:
            print('[!] Asynchroneous video capturing has already been started.')
            return None
        self.started = True
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.started:
            #s = time.time()
            self.grabbed, self.frame = self.cap.read()
            #print(1/(time.time() - s))

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
        return frame

    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exec_type, exc_value, traceback):
        self.cap.release()

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")


@app.route("/video_feed")
def video_feed():
    return Response(generate(),
                    mimetype = "multipart/x-mixed-replace; boundary=frame")

def generate():
  c = WebcamVideoStream(0)
  c.start()
  while True:
    with lock:
      img = c.read()
    if img is None:
      continue
    img = recognition(img)
    (flag, encodedImage) = cv2.imencode(".jpg", img)
    if not flag:
      continue
    yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(encodedImage) + b'\r\n')
	
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True, use_reloader=False)
        
            
            
        
            
        
