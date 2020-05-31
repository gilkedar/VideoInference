import argparse
import os
import threading

from Utils.Settings import Config
from Utils.Helpers.Logger import Logger

from Utils.Exceptions.InputErrors.Errors import ErrorInvalidInputVideoPath
from Utils.Exceptions.InputErrors.Errors import ErrorInvalidInputAlgorithmChoice
from Utils.Exceptions.InputErrors.Errors import ErrorInvalidProtocolChoice
from Utils.Exceptions.InputErrors.Errors import ErrorEnvVarNotSet

from Client.RequestsManager import RequestsManager
from Utils.Helpers.Video.VideoFileFrameExtractor import VideoFileFrameExtractor
from Utils.Helpers.Video.DriverFrameExtractor import DriverFrameExtractor

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

ap.add_argument("-p", "--protocol", required=False, type=str, default=Config.PROTOCOL_HTTP,
                help="Protocol to send image to server of the desired server")

input_arguments = vars(ap.parse_args())

# add "-f C:\Users\gilke\GitHubProjects\VideoInference\Tests\VideoTestFile\soccer.mp4" input param to run video file


class MainClient:

    def __init__(self, input_params):
        self.input_params = input_params

        self.server_ip = None
        self.image_protocol = None
        self.desired_algorithm = None
        self.video_file_path = None

        self.requests_manager = None
        self.frame_extractor = None
        self.requests_publisher = None

        self.condition_received_all_requests = threading.Condition()
        self.logger = Logger(self.__class__.__name__)

    def validateEnvVariables(self):
        if Config.ENV_VAR_MQTT_TOKEN not in os.environ:
            raise ErrorEnvVarNotSet(Config.ENV_VAR_MQTT_TOKEN)
        Config.MQTT_SERVER_IP = os.environ[Config.ENV_VAR_MQTT_TOKEN]

    def initResources(self):
        self.validateEnvVariables()
        self.validateInputParams()
        self.initImagePublisher()
        # self.readServer-Parameters() @TODO - add routine to read info from DB

        self.requests_manager = RequestsManager(self.desired_algorithm,self.condition_received_all_requests)

        if self.video_file_path:
            self.frame_extractor = VideoFileFrameExtractor(self.video_file_path)
        else:
            self.frame_extractor = DriverFrameExtractor()

    def closeResources(self):
        self.requests_manager.closeResources()
        self.requests_manager = None
        self.requests_publisher = None
        self.frame_extractor.closeSource()
        self.frame_extractor = None

    def validateInputParams(self):
        self.validateAlgorithmInput()
        self.validateImageProtocolInput()
        self.validateIpAddressInput()
        self.validateVideoPathInput()

    def validateAlgorithmInput(self):
        algorithm_name = self.input_params[Config.INPUT_PARAM_ALGORITHM_NAME]
        # validate algorithm name
        if algorithm_name != Config.ALGORITHM_IS_SANTA:
            raise ErrorInvalidInputAlgorithmChoice(algorithm_name)
        self.desired_algorithm = algorithm_name

    def validateVideoPathInput(self):
        self.video_file_path = self.input_params[Config.INPUT_PARAM_VIDEO_FILE_NAME]
        # validate video path
        if self.video_file_path:
            if not os.path.exists(self.video_file_path):
                raise ErrorInvalidInputVideoPath(self.video_file_path)


    def validateIpAddressInput(self):
        self.server_ip = self.input_params[Config.INPUT_PARAM_IP_ADDRESS_NAME]

    def validateImageProtocolInput(self):
        self.image_protocol = self.input_params[Config.INPUT_PARAM_PROTOCOL_NAME]

    def initImagePublisher(self):
        if self.image_protocol == Config.PROTOCOL_ZMQ:
            self.requests_publisher = ZmqImagePublisher(self.server_ip)
        elif self.image_protocol == Config.PROTOCOL_HTTP:
            self.requests_publisher = HttpImagePublisher(self.server_ip)
        else:
            raise ErrorInvalidProtocolChoice(self.image_protocol)

    def publishRequest(self,req_msg):
        # self.logger.info("Publishing request : {}".format(req_msg.request_id))
        self.requests_publisher.publish(req_msg)

    def notifyEndOfFrames(self):
        self.logger.info("Finished sending all frames to server")
        self.requests_manager.setEndOfFrames()

    def run(self):
        # initialize client resources
        self.logger.info("Initializing Client Resources...")
        self.initResources()

        # start listening
        self.requests_manager.startListeningToIncomingResponses()
        self.logger.info("Client starting to publish frames...")

        while True:
            # Read frame by frame
            frame_id, frame = self.frame_extractor.getNextFrame()

            if self.frame_extractor.finished:
                break

            # generate relevant request
            req_msg = self.requests_manager.generateRequestMessage(frame_id,frame)
            # publish request
            threading.Thread(target=self.publishRequest,args=(req_msg,)).start()


        self.notifyEndOfFrames()
        self.logger.info("Waiting for all requests to arrive...")
        with self.condition_received_all_requests:
            self.condition_received_all_requests.wait()
        self.logger.info("Finished all requests...Shutting down client...")


if __name__ == "__main__":
    main_client = MainClient(input_arguments)
    main_client.run()
    main_client.closeResources()
