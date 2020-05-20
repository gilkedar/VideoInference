import argparse
import os

from Utils.Settings import Config
from Utils.Exceptions.Errors import ErrorInvalidInputVideoPath
from Utils.Exceptions.Errors import ErrorInvalidInputAlgorithmChoice
from Utils.Exceptions.Errors import ErrorInvalidProtocolChoice

from Client.RequestsManager import RequestsManager
from Client.VideoPlayer import VideoPlayer

from Utils.Infrastructure.ImageProtocols.ZMQ.ZmqImagePublisher import ZmqImagePublisher
from Utils.Infrastructure.ImageProtocols.HTTP.HttpImagePublisher import HttpImagePublisher

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-a", "--algorithm", required=True, type=str,
                help="Desired deep Learning algorithm to get inference from cloud resources")

ap.add_argument("-f", "--videofile", required=False,type=str, default=None,
                help="Full Path to desired video file. If no path chosen, read from camera driver")

ap.add_argument("-i", "--ip", required=False, type=str, default=Config.LOCALHOST_IP,
                help="IP of the desired server")

ap.add_argument("-p", "--protocol", required=False, type=str, default=Config.PROTOCOL_ZMQ,
                help="Protocol to send image to server of the desired server")

input_arguments = vars(ap.parse_args())


class MainClient:

    def __init__(self, input_params):
        self.input_params = input_params

        self.server_ip = None
        self.image_protocol = None
        self.desired_algorithm = None
        self.video_file_path = None

        self.requests_manager = None
        self.video_player = None
        self.requests_publisher = None

        # self.readServerParameters() @TODO - add routine to read info from DB
        self.setInputParams(input_params)
        self.initResources()
        self.initImagePublisher()

    def setInputParams(self,params):
        algorithm_name = params[Config.INPUT_PARAM_ALGORITHM_NAME]

        # validate video path
        if Config.INPUT_PARAM_VIDEO_FILE_NAME in params:
            self.video_file_path = params[Config.INPUT_PARAM_VIDEO_FILE_NAME]
            if not os.path.exists(self.video_file_path):
                raise ErrorInvalidInputVideoPath(self.video_file_path)

        # validate algorithm name
        if algorithm_name != Config.ALGORITHM_IS_SANTA:
            raise ErrorInvalidInputAlgorithmChoice(algorithm_name)
        self.desired_algorithm = algorithm_name

        # validate ip address
        if Config.INPUT_PARAM_IP_ADDRESS_NAME in params:
            self.server_ip = params[Config.INPUT_PARAM_IP_ADDRESS_NAME]

        # validate image protocol
        if Config.INPUT_PARAM_PROTOCOL_NAME in params:
            self.image_protocol = params[Config.INPUT_PARAM_PROTOCOL_NAME]

        # validate image protocol
        if Config.INPUT_PARAM_PROTOCOL_NAME in params:
            self.image_protocol = params[Config.INPUT_PARAM_PROTOCOL_NAME]


    def initResources(self):
        self.requests_manager = RequestsManager(self.desired_algorithm)
        self.video_player = VideoPlayer(self.video_file_path)

    def initImagePublisher(self):
        if self.image_protocol == Config.PROTOCOL_ZMQ:
            self.requests_publisher = ZmqImagePublisher(self.server_ip)
        elif self.image_protocol == Config.PROTOCOL_HTTP:
            self.requests_publisher = HttpImagePublisher(self.server_ip)
        else:
            raise ErrorInvalidProtocolChoice(self.image_protocol)

    def run(self):
        # Open video source
        self.video_player.openSource()
        self.requests_manager.startListeningToIncomingResponses()

        while not self.video_player.finished:
            # Read frame by frame
            img = self.video_player.getNextFrame()
            # generate relevant request
            req_msg = self.requests_manager.generateRequest(img)
            # publish request
            self.requests_publisher.publish(req_msg)

        pass


if __name__ == "__main__":
    main_client = MainClient(input_arguments)
    main_client.run()
