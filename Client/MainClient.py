import argparse
import os
import threading
from Utils.Settings import Config
from Utils.Exceptions.Errors import ErrorInvalidInputVideoPath
from Utils.Exceptions.Errors import ErrorInvalidInputAlgorithmChoice
from Utils.Exceptions.Errors import ErrorInvalidProtocolChoice

from Client.RequestsManager import RequestsManager
from Client.VideoFrameExtractor import VideoFrameExtractor

from Utils.Infrastructure.ImageProtocols.ZMQ.ZmqImagePublisher import ZmqImagePublisher
from Utils.Infrastructure.ImageProtocols.HTTP.HttpImagePublisher import HttpImagePublisher

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-a", "--algorithm", required=True, type=str,
                help="Desired deep Learning algorithm to get inference from cloud resources")

ap.add_argument("-f", "--videofile", required=False,type=str,
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
        self.video_frame_extractor = None
        self.requests_publisher = None

        self.condition_received_all_requests = threading.Condition()

    def initResources(self):
        self.setInputParams(self.input_params)
        # self.readServerParameters() @TODO - add routine to read info from DB
        self.requests_manager = RequestsManager(self.desired_algorithm,self.condition_received_all_requests)
        self.video_frame_extractor = VideoFrameExtractor(self.video_file_path)
        self.initImagePublisher()

    def closeResources(self):
        self.requests_manager.closeResources()
        self.requests_manager = None
        self.requests_publisher = None
        self.video_frame_extractor.closeSource()
        self.video_frame_extractor = None

    def getAlgorithmName(self):
        return self.desired_algorithm

    def setInputParams(self,params):
        algorithm_name = params[Config.INPUT_PARAM_ALGORITHM_NAME]
        video_file_path = params[Config.INPUT_PARAM_VIDEO_FILE_NAME]

        # validate video path
        if Config.INPUT_PARAM_VIDEO_FILE_NAME in params:
            if video_file_path:
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


    def initImagePublisher(self):
        if self.image_protocol == Config.PROTOCOL_ZMQ:
            self.requests_publisher = ZmqImagePublisher(self.server_ip)
        elif self.image_protocol == Config.PROTOCOL_HTTP:
            self.requests_publisher = HttpImagePublisher(self.server_ip)
        else:
            raise ErrorInvalidProtocolChoice(self.image_protocol)

    def publishRequest(self,req_msg):
        self.requests_publisher.publish(req_msg)

    def notifyEndOfFrames(self):
        print("Finished sending all frames")
        self.requests_manager.setEndOfFrames()

    def run(self):
        # initialize client resources
        self.initResources()
        # start listening
        self.requests_manager.startListeningToIncomingResponses()

        while True:
            # Read frame by frame
            frame_id, frame = self.video_frame_extractor.getNextFrame()

            if self.video_frame_extractor.finished:
                break
            # generate relevant request
            req_msg = self.requests_manager.generateRequestMessage(frame_id,frame)
            # publish request
            self.publishRequest(req_msg)

            if frame_id == 10: # for debugging purposes
                break

        self.notifyEndOfFrames()
        print("Waiting for all requests")
        with self.condition_received_all_requests:
            self.condition_received_all_requests.wait()
        print("Finished all requests")


if __name__ == "__main__":
    main_client = MainClient(input_arguments)
    main_client.run()
    main_client.closeResources()
