import argparse
import os
import atexit

from Utils.Settings import Config
from Utils.Helpers.Logger import Logger

from Server.ResponsesManager import ResponsesManager
from Utils.Infrastructure.ImageProtocols.HTTP.HttpImageSubscriber import HttpImageSubscriber

from flask import Flask, request, Response


app = Flask(__name__)


class HttpMainServer:

    def __init__(self):
        self.response_manager = None
        self.requests_subscriber = None
        self.logger = Logger(self.__class__.__name__)

    def closeResources(self):
        self.requests_subscriber = None
        self.response_manager.closeResources()
        self.response_manager = None

    def initResources(self):
        # initialize response manager
        self.response_manager = ResponsesManager()
        # connect to request subscriber
        self.initImageSubscriber()

        atexit.register(self.closeResources)

    def initImageSubscriber(self):
        self.requests_subscriber = HttpImageSubscriber(self.response_manager.handleNewRequest)

    def run(self):
        self.logger.info("Initializing Resources...")
        self.initResources()
        self.logger.info("Ready for incoming requests...")


@app.route("/", methods=['POST'])
def func():
    try:
        r = request

        msg = http_main_server.requests_subscriber.decodeIncomingRequest(r)
        # main_server.logger.info("got msg - {}".format(msg.request_id))
        # threading.Thread(target=main_server.response_manager.handleNewRequest, args=(msg,)).start()
        ans = http_main_server.response_manager.handleNewRequest(msg)
        return Response(response="Image Request ({}) Received in HttpServer {}".format(msg.request_id, ans.serialize()),
                        status=200,
                        mimetype="text/plain")
    except Exception as ex:
        http_main_server.logger.error("*** SERVER ERROR *** ")
        return Response(response="{}".format(ex),
                        status=444,
                        mimetype="text/plain")


if __name__ == "__main__":

    http_main_server = HttpMainServer()
    http_main_server.run()
    try:
        app.run(host=Config.GLOBAL_IP, port=Config.HTTP_PORT)
    except Exception as ex:
        http_main_server.logger.critical(ex)
    finally:
        http_main_server.closeResources()

