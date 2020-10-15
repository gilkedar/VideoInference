import argparse
import atexit
import threading

from Utils.Settings import Config
from Utils.Helpers.Logger import Logger

from Server.RequestsManager import RequestsManager

from Utils.Infrastructure.ImageProtocols.HTTP.HttpImageSubscriber import HttpImageSubscriber
from Utils.Helpers.Video.FrameEditor import FrameEditor

from flask import Flask, request, Response, render_template

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--algorithm", required=True, type=str,
                help="Algorithm to run on http server")
input_arguments = vars(ap.parse_args())


app = Flask(__name__)


class HttpMainServer:

    def __init__(self, algorithm_name):
        self.algorithm_name = algorithm_name
        self.requests_manager = None
        self.requests_subscriber = None
        self.logger = Logger(self.__class__.__name__)
        self.output_lock = threading.Lock()
        self.output_image = None
        self.frame_editor = FrameEditor()

    def closeResources(self):
        self.requests_subscriber = None
        self.requests_manager.closeResources()
        self.requests_manager = None

    def initResources(self):
        # initialize response manager
        self.requests_manager = RequestsManager(self.algorithm_name)
        # connect to request subscriber
        self.requests_subscriber = HttpImageSubscriber(self.requests_manager.handleNewRequest)

        atexit.register(self.closeResources)

    def getOutputImage(self):
        with self.output_lock:
            return self.output_image

    def updateOutputImage(self, updated_image):
        with self.output_lock:
            self.output_image = updated_image

    def genearteOutputImage(self):
        while True:
            output_frame = self.getOutputImage()
            if output_frame is None:
                continue
            encoded_image = self.frame_editor.encode_to_jpg(output_frame)
            if encoded_image is not None:
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                       bytearray(encoded_image) + b'\r\n')


    def run(self):
        self.logger.info("Initializing Resources...")
        self.initResources()
        self.logger.info("Ready for incoming requests...")


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(http_main_server.genearteOutputImage(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")



@app.route("/", methods=['GET'])
def video_func():

    try:
        r = request

        request_msg = http_main_server.requests_subscriber.decodeIncomingRequest(r)
        # threading.Thread(target=http_main_server.response_manager.handleNewRequest, args=(request_msg,)).start()
        response = http_main_server.requests_manager.handleNewRequest(request_msg)
        # http_main_server.updateOutputImage(response.updated_frame)
        return Response(response=response.toJSON(),
                        status=222,
                        mimetype="application/json")
    except Exception as ex:
        http_main_server.logger.error(f"SERVER ERROR : {ex} ")
        return Response(response=f"Failed - Request  - {ex.message}",
                        status=444,
                        mimetype="text/plain")


@app.route("/test")
def func():

    return render_template("index.html")


if __name__ == "__main__":

    http_main_server = HttpMainServer(input_arguments[Config.INPUT_PARAM_ALGORITHM_NAME])
    http_main_server.run()
    try:
        app.run(host=Config.GLOBAL_IP, port=Config.HTTP_PORT)
    except Exception as ex:
        http_main_server.logger.critical(ex)
    finally:
        http_main_server.closeResources()
