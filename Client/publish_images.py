from flask import Flask, render_template, Response
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from imutils.video import VideoStream
import time
import cv2
import threading
import requests
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", type=str, required=True, help="ip address of the device")
ap.add_argument("-p", "--port", type=str, required=True, help="ephemeral port number of the server (1024 to 65535)")
ap.add_argument("-a", "--api", type=str, required=False,default="", help="enter the desired API uri")
args = vars(ap.parse_args())

request_id = 0


def publish_image(frame, address):
    global request_id
    request_id += 1
    content_type = 'image/jpeg'
    headers = {'content-type': content_type,
               'user_id': "gilkedar",
               'algorithm': "detect_faces",
               'request_id': str(request_id)}
    # resized_frame = imutils.resize(frame, width=400)
    (flag, encodedImage) = cv2.imencode(".jpg", frame)
    bytes_str = encodedImage.tostring()
    requests.post(address, data=bytes_str, headers=headers)

    print(request_id)

def gen():
    """Video streaming generator function."""
    vs = VideoStream(src=0).start()
    time.sleep(2.0)
    address = "http://{}:{}{}".format(args["ip"], args["port"], args["api"])
    while True:
        frame = vs.read()
        threading.Thread(target=publish_image(frame, address)).start()


if __name__ == '__main__':
    gen()