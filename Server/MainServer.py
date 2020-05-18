import argparse
from Utils.Settings import Config
from Server.ResponsesManager import ResponsesManager
from Utils.Protocols.MQTT.MqttSubscriber import MqttSubscriber
from Utils.Protocols.HTTP.HttpSubscriber import HttpSubscriber
from Utils.Protocols.ZMQ.ZmqSubscriber import ZmqSubscriber
from Utils.Exceptions.Errors import ErrorInvalidProtocolChoice

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-p", "--protocol", required=False, type=str, default=Config.PROTOCOL_ZMQ,
                help="Protocol to send image to server of the desired server")

input_arguments = vars(ap.parse_args())



class MainServer:

    def __init__(self, params):
        self.input_params = params

        self.response_manager = None
        self.image_transport_protocol = None
        self.requests_subscriber = None

        self.setInputParams(params)
        self.initResources()


    def initResources(self):
        # initialize response manager
        self.response_manager = ResponsesManager()

        # connect to request subscriber
        self.initSubscriber()

    def setInputParams(self, params):

        # validate image protocol
        if Config.INPUT_PARAM_PROTOCOL_NAME in params:
            self.image_transport_protocol = params[Config.INPUT_PARAM_PROTOCOL_NAME]

    def initSubscriber(self):
        if self.image_transport_protocol == Config.PROTOCOL_ZMQ:
            self.requests_subscriber = ZmqSubscriber(self.vhandleIncomingRequests)
        elif self.image_transport_protocol == Config.PROTOCOL_MQTT:
            self.requests_subscriber = MqttSubscriber(self.handleIncomingRequests)
        elif self.image_transport_protocol == Config.PROTOCOL_HTTP:
            self.requests_subscriber = HttpSubscriber(self.handleIncomingRequests)
        else:
            raise ErrorInvalidProtocolChoice(self.image_transport_protocol)

    def run(self):
        self.requests_subscriber.subscribe()


if __name__ == "__main__":
    main_server = MainServer(input_arguments)
    main_server.run()

