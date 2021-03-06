import argparse
import os
import atexit

from Utils.Settings import Config
from Utils.Helpers.Logger import Logger

from Server.RequestsManager import RequestsManager

from Utils.Infrastructure.ImageProtocols.HTTP.HttpImageSubscriber import HttpImageSubscriber
from Utils.Infrastructure.ImageProtocols.ZMQ.ZmqImageSubscriber import ZmqImageSubscriber

from Utils.Exceptions.InputErrors.Errors import ErrorInvalidProtocolChoice
from Utils.Exceptions.InputErrors.Errors import ErrorEnvVarNotSet

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-p", "--protocol", required=False, type=str, default=Config.PROTOCOL_ZMQ,
                help="Protocol to send image to server of the desired server")

input_arguments = vars(ap.parse_args())


class MainServer:

    def __init__(self, params):
        self.input_params = params

        self.image_protocol = None

        self.response_manager = None
        self.requests_subscriber = None

        self.logger = Logger(self.__class__.__name__)

    def closeResources(self):
        self.requests_subscriber = None
        self.response_manager.closeResources()
        self.response_manager = None

    def validateEnvVariables(self):
        if Config.ENV_VAR_MQTT_TOKEN not in os.environ:
            raise ErrorEnvVarNotSet(Config.ENV_VAR_MQTT_TOKEN)
        Config.MQTT_SERVER_IP = os.environ[Config.ENV_VAR_MQTT_TOKEN]

    def initResources(self):
        # validate input parameters
        self.validateInputParams()
        # initialize response manager
        self.response_manager = RequestsManager()
        # connect to request subscriber
        self.initImageSubscriber()

        atexit.register(self.closeResources)

    def validateInputParams(self):
        # validate environmental Variables are set
        self.validateEnvVariables()

        # validate image protocol
        if Config.INPUT_PARAM_PROTOCOL_NAME in self.input_params:
            self.image_protocol = self.input_params[Config.INPUT_PARAM_PROTOCOL_NAME]

    def initImageSubscriber(self):
        if self.image_protocol == Config.PROTOCOL_ZMQ:
            self.requests_subscriber = ZmqImageSubscriber(Config.LOCALHOST_IP, self.response_manager.handleNewRequest)
        elif self.image_protocol == Config.PROTOCOL_HTTP:
            self.requests_subscriber = HttpImageSubscriber(self.response_manager.handleNewRequest)
        else:
            raise ErrorInvalidProtocolChoice(self.image_protocol)

    def run(self):
        self.logger.info("Initializing Resources...")
        self.initResources()
        self.logger.info("Ready for incoming requests...")
        self.requests_subscriber.subscribe()


if __name__ == "__main__":
    main_server = MainServer(input_arguments)
    try:
        main_server.run()
    except Exception as ex:
        main_server.logger.critical(ex)
    main_server.closeResources()

