from __future__ import print_function
from flask import Flask, Response
from pyzbar import pyzbar
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime

import numpy as np
import cv2
import time


camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

app = Flask(__name__)


@app.route('/stream')
def stream():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def get_frame():
    camera.capture(rawCapture, format="bgr", use_video_port=True)
    frame = rawCapture.array
    process_frame(frame)
    ret, jpeg = cv2.imencode('.jpg', frame)
    rawCapture.truncate(0)

    return jpeg.tobytes()
    
def process_frame(frame):
    decoded_objs = decode(frame)
    draw_positions(frame, decoded_objs)

def decode(frame):
    decoded_objs = pyzbar.decode(frame, scan_locations=True)
    for decoded_obj in decoded_objs:
        print(datetime.now().strftime('%H:%M:%S.%f'))
        print('Type: ', decoded_obj.type)
        print('Data: ', decoded_obj.data)
    
    return decoded_objs
        
def draw_positions(frame, decoded_objs):
    for decoded_obj in decoded_objs:
        left, top, width, height = decoded_obj.rect
        frame = cv2.rectangle(frame,
                              (left, top),
                              (left + width, height + top),
                              (0, 255, 0), 2)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, threaded=True)
