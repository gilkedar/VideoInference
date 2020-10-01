from flask import Flask, render_template, Response
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from imutils.video import VideoStream
import time
import imutils
import cv2
import threading
import requests
import json

counter = 0

def publish_image(frame, address):
    global counter
    counter += 1
    content_type = 'image/jpeg'
    headers = {'content-type': content_type,
               'user_id': "gilkedar",
               'algorithm': "detect_faces",
               'blabla': 'blablabla'}
    # resized_frame = imutils.resize(frame, width=400)
    (flag, encodedImage) = cv2.imencode(".jpg", frame)

    requests.post(address, data=encodedImage.tostring(), headers=headers)
    print(counter)

def gen():
    """Video streaming generator function."""
    vs = VideoStream(src=0).start()
    time.sleep(2.0)



    address = "http://127.0.0.1:5000/user"
    # test_url = addr + '/api/test'

    while True:
        frame = vs.read()
        threading.Thread(target=publish_image(frame, address)).start()

if __name__ == '__main__':
    gen()