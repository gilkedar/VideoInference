import threading

from Utils.Helpers.TimerManager import TimerManager
from Utils.Helpers.Timers.InferenceTimer import InferenceMessageTimer
from Utils.Helpers.Logger import Logger
from Utils.Settings import Config

from Utils.Infrastructure.DataProtocols.MQTT.MqttDataPublisher import MqttDataPublisher
from Server.InferenceManager import InferenceManager


class ResponsesManager:

    # holds requests objects by request_id
    open_requests = {}

    def __init__(self):

        self.logger = Logger(self.__class__.__name__)
        self.requests_lock = threading.Lock()
        self.inference_manager = InferenceManager()
        self.response_publisher = MqttDataPublisher(Config.MQTT_SERVER_IP, Config.MQTT_TOPIC_NAME)
        self.timer_manager = TimerManager()

    def closeResources(self):
        self.inference_manager = None
        self.response_publisher = None
        self.timer_manager.printTimers()
        self.timer_manager = None

    def addRequest(self,request_msg):
        with self.requests_lock:
            ResponsesManager.open_requests[request_msg.request_id] = request_msg
            self.logger.info("Adding request : {}".format(request_msg.request_id))
            self.timer_manager.startMessageTimer(InferenceMessageTimer(request_msg.request_id, request_msg.algorithm))

    def removeRequest(self,request_id):
        with self.requests_lock:
            self.timer_manager.stopMessageTimer(request_id)
            del ResponsesManager.open_requests[request_id]
            self.logger.info("Removing request : {}".format(request_id))

    def publishResponse(self,response):
        self.response_publisher.publish(response)

    def handleNewRequest(self, request_message):
        self.addRequest(request_message)
        desired_algorithm_name = request_message.algorithm
        algorithm = self.inference_manager.getAlgorithmInstanceFromName(desired_algorithm_name)
        ans = algorithm.run(request_message)
        response_message = algorithm.generateResponseMessage(request_message, ans)
        self.publishResponse(response_message)
        self.removeRequest(response_message.request_id)
        return ans
