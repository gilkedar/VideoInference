import threading

from Utils.Helpers.TimerManager import TimerManager
from Utils.Helpers.Timers.InferenceTimer import InferenceMessageTimer
from Utils.Helpers.Logger import Logger
from Utils.Settings import Config
from Utils.Exceptions.ServerErrors.SererErrors import ErrorInvalidAlgorithm
from Utils.Infrastructure.DataProtocols.MQTT.MqttDataPublisher import MqttDataPublisher
from Utils.Helpers.Video.FrameEditor import FrameEditor

from Server.InferenceManager import InferenceManager


class RequestsManager:

    # holds requests objects by request_id
    open_requests = {}

    def __init__(self, algorithm_name):
        self.algorithm_name = algorithm_name
        self.logger = Logger(self.__class__.__name__)
        self.requests_lock = threading.Lock()
        self.inference_manager = InferenceManager(self.algorithm_name)
        # self.response_publisher = MqttDataPublisher(Config.MQTT_SERVER_IP, Config.MQTT_TOPIC_NAME)
        self.timer_manager = TimerManager()
        self.frame_editor = FrameEditor()

    def closeResources(self):
        self.inference_manager = None
        self.response_publisher = None
        self.timer_manager.printTimers()
        self.timer_manager = None

    def addRequest(self,request_msg):
        with self.requests_lock:
            RequestsManager.open_requests[request_msg.request_id] = request_msg
            self.logger.info("Adding request : {}".format(request_msg.request_id))
            self.timer_manager.startMessageTimer(InferenceMessageTimer(request_msg.request_id, request_msg.algorithm))

    def removeRequest(self,request_id):
        with self.requests_lock:
            self.timer_manager.stopMessageTimer(request_id)
            del RequestsManager.open_requests[request_id]
            self.logger.info("Removing request : {}".format(request_id))

    def publishResponse(self,response):
        self.response_publisher.publish(response)

    def validateRequest(self, request_message):
        algorithm = request_message.algorithm
        if algorithm != self.algorithm_name:
            raise ErrorInvalidAlgorithm(algorithm)

    def handleNewRequest(self, request_message):
        self.validateRequest(request_message)
        self.addRequest(request_message)
        ans = self.inference_manager.getInference(request_message)
        response_message = self.inference_manager.getAlgorithm().generateResponseMessage(request_message, ans)
        # self.publishResponse(response_message)
        self.removeRequest(response_message.request_id)
        return response_message
