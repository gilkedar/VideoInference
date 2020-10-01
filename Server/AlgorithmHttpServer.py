import argparse
import atexit
import cv2
import threading
import json
import imutils
import numpy

from Utils.Settings import Config
from Utils.Helpers.Logger import Logger

from Server.ResponsesManager import ResponsesManager
from Utils.Infrastructure.ImageProtocols.HTTP.HttpImageSubscriber import HttpImageSubscriber

from flask import Flask, request, Response, render_template

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-a", "--algorithm", required=True, type=str,
                help="Algorithm to run on http server")

input_arguments = vars(ap.parse_args())

app = Flask(__name__)

outputFrame = None
lock = threading.Lock()

class HttpMainServer:

    def __init__(self, algorithm_name):
        self.algorithm_name = algorithm_name
        self.response_manager = None
        self.requests_subscriber = None
        self.logger = Logger(self.__class__.__name__)

    def closeResources(self):
        self.requests_subscriber = None
        self.response_manager.closeResources()
        self.response_manager = None

    def initResources(self):
        # initialize response manager
        self.response_manager = ResponsesManager(self.algorithm_name)
        # connect to request subscriber
        self.initImageSubscriber()

        atexit.register(self.closeResources)

    def initImageSubscriber(self):
        self.requests_subscriber = HttpImageSubscriber(self.response_manager.handleNewRequest)

    def run(self):
        self.logger.info("Initializing Resources...")
        self.initResources()
        self.logger.info("Ready for incoming requests...")

#
def generate():
    global outputFrame, lock

    while True:
        # wait until the lock is acquired
        with lock:
            if outputFrame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            if not flag:
                continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/user", methods=['POST'])
def video_func():
    global outputFrame

    r = request
    # frame = numpy.array(json.loads(r.data)["image_data"])

    img_str = r.data
    img = numpy.frombuffer(img_str, numpy.uint8)
    frame = cv2.imdecode(img, flags=1)
    algorithm = r.headers.environ['HTTP_ALGORITHM']
    with lock:
        outputFrame = frame
    return Response()

@app.route("/")
def func():

    return render_template("index.html")

#
#
# @app.route("/", methods=['POST'])
# def func():
#     try:
#         r = request
#
#         msg = http_main_server.requests_subscriber.decodeIncomingRequest(r)
#         # main_server.logger.info("got msg - {}".format(msg.request_id))
#         # threading.Thread(target=main_server.response_manager.handleNewRequest, args=(msg,)).start()
#         response = http_main_server.response_manager.handleNewRequest(msg)
#         return Response(response=response.toJSON(),
#                         status=200,
#                         mimetype="application/json")
#     except Exception as ex:
#         http_main_server.logger.error(f"SERVER ERROR : {ex} ")
#         return Response(response="{}".format(ex),
#                         status=444,
#                         mimetype="text/plain")
#

if __name__ == "__main__":

    http_main_server = HttpMainServer(input_arguments[Config.INPUT_PARAM_ALGORITHM_NAME])
    http_main_server.run()
    try:
        app.run(host=Config.GLOBAL_IP, port=Config.HTTP_PORT)
    except Exception as ex:
        http_main_server.logger.critical(ex)
    finally:
        http_main_server.closeResources()
