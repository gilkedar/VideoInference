from Utils.Settings import Config
from Utils.Infrastructure.DataProtocols.MQTT.MqttDataPublisher import MqttDataPublisher
from Utils.Messages.Responses.ResponseMessage import ResponsetMessage
from Server.InferenceManager import InferenceManager
import threading


class ResponsesManager:

    # holds requests objects by request_id
    open_requests = {}

    def __init__(self):
        self.inference_manager = None
        self.response_publisher = None
        self.requests_lock = threading.Lock()
        self.initResources()

    def initResources(self):
        self.inference_manager = InferenceManager()
        self.response_publisher = MqttDataPublisher(Config.MQTT_TOPEN_IP, Config.MQTT_TOPIC_NAME)

    def addRequest(self,request_msg):
        with self.requests_lock:
            ResponsesManager.open_requests[request_msg.request_id] = request_msg
            print("Adding request : {}".format(request_msg.request_id))

    def removeRequest(self,request_id):
        with self.requests_lock:
            del ResponsesManager.open_requests[request_id]
            print("Removing request : {}".format(request_id))

    def publishResponse(self,response):
        self.response_publisher.publish(response)

    def handleNewRequest(self, request_message):
        self.addRequest(request_message)
        desired_algorithm_name = request_message.algorithm
        algorithm = self.inference_manager.getAlgorithmInstanceFromName(desired_algorithm_name)
        ans = algorithm.run(request_message.data)
        response_message = algorithm.generateResponseMessage(request_message,ans)
        self.publishResponse(response_message)
        self.removeRequest(response_message.request_id)