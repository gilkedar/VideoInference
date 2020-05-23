import argparse
from Utils.Settings import Config
from Server.ResponsesManager import ResponsesManager
from Utils.Infrastructure.ImageProtocols.HTTP.HttpImageSubscriber import HttpImageSubscriber
from Utils.Infrastructure.ImageProtocols.ZMQ.ZmqImageSubscriber import ZmqImageSubscriber
from Utils.Exceptions.InputErrors.Errors import ErrorInvalidProtocolChoice

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-p", "--protocol", required=False, type=str, default=Config.PROTOCOL_ZMQ,
                help="Protocol to send image to server of the desired server")

input_arguments = vars(ap.parse_args())



class MainServer:

    def __init__(self, params):
        self.input_params = params

        self.response_manager = None
        self.image_protocol = None
        self.requests_subscriber = None

        self.validateInputParams(params)
        self.initResources()


    def initResources(self):
        # initialize response manager
        self.response_manager = ResponsesManager()

        # connect to request subscriber
        self.initImageSubscriber()

    def validateInputParams(self, params):

        # validate image protocol
        if Config.INPUT_PARAM_PROTOCOL_NAME in params:
            self.image_protocol = params[Config.INPUT_PARAM_PROTOCOL_NAME]

    def initImageSubscriber(self):
        if self.image_protocol == Config.PROTOCOL_ZMQ:
            self.requests_subscriber = ZmqImageSubscriber(Config.LOCALHOST_IP, self.response_manager.handleNewRequest)
        elif self.image_protocol == Config.PROTOCOL_HTTP:
            self.requests_subscriber = HttpImageSubscriber(self.response_manager.handleNewRequest)
        else:
            raise ErrorInvalidProtocolChoice(self.image_protocol)

    def run(self):
        print("Listening to incoming image requests...")
        self.requests_subscriber.subscribe()


if __name__ == "__main__":
    main_server = MainServer(input_arguments)
    main_server.run()

