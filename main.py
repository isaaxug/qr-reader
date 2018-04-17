from __future__ import print_function
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


def decode(image):
    decoded_objs = pyzbar.decode(image, scan_locations=True)
    for obj in decoded_objs:
        print(datetime.now().strftime('%H:%M:%S.%f'))
        print('Type: ', obj.type)
        print('Data: ', obj.data)
    
    return decoded_objs
        
def display(image, decoded_objs):
    for decoded_obj in decoded_objs:
        left, top, width, height = decoded_obj.rect
        image = cv2.rectangle(image,
                              (left, top),
                              (left + width, height + top),
                              (0, 255, 0), 2)
    return image
    
if __name__ == '__main__':
    for frame in camera.capture_continuous(rawCapture,
                                           format="bgr",
                                           use_video_port=True):
        image = frame.array
        decoded_objs = decode(image)
        image = display(image, decoded_objs)
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)

        if key == ord("q"):
            break
        
