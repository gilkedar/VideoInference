from Utils.Settings import Config
from Utils.Infrastructure.DataProtocols.MQTT.MqttDataPublisher import MqttDataPublisher
from Utils.Messages.Responses.ResponseMessage import ResponsetMessage
from Server.InferenceManager import InferenceManager


class ResponsesManager:

    # holds requests objects by request_id
    open_requests = {}

    def __init__(self):
        self.inference_manager = None
        self.response_publisher = None

    def initResources(self):
        self.inference_manager = InferenceManager()
        self.response_publisher = MqttDataPublisher(Config.MQTT_TOPIC_NAME)

    def addRequest(self,request_msg):
        # @TODO add mutex to open_requests object
        ResponsesManager.open_requests[request_msg.request_id] = request_msg

    def removeRequest(self,request_id):
        # @TODO add mutex to open_requests object
        del ResponsesManager.open_requests[request_id]

    def publishResponse(self,response):
        self.response_publisher.publish(response)

    def handleNewRequest(self, request_message):

        self.addRequest(request_message.request_id)
        desired_algorithm_name = request_message.algorithm
        algorithm = self.inference_manager.getAlgorithmInstanceFromName(desired_algorithm_name)
        ans = algorithm.run(request_message.data)
        response_message = algorithm.generateResponseMessage(request_message,ans)
        self.publishResponse(response_message)
        self.removeRequest(response_message.request_id)