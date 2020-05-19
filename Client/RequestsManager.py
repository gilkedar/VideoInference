from Utils.Infrastructure.DataProtocols.MQTT.MqttDataSubscriber import MqttDataSubscriber
from Utils.Messages.RequestsMessageFactory import RequestsMessageFactory
import threading


class RequestsManager:

    # holds requests objects by request_id
    open_requests = {}

    def __init__(self, image_protocol, algorithm):
        self.image_protocol = image_protocol
        self.algorithm = algorithm

        self.listen_flag = False
        self.response_subscriber = None
        self.factory = None

    def initResources(self):
        self.factory = RequestsMessageFactory()
        self.response_subscriber = MqttDataSubscriber(self.handleIncomingResponses)

    def startListeningToIncomingResponses(self):
        threading.Thread(self.response_subscriber.subscribe,args=(self.response_subscriber,)).start()


    def generateRequestMessage(self,image):
        request_msg = self.factory.createRequest(image, self.algorithm)
        self.addRequest(request_msg)
        return request_msg

    def addRequest(self,request_msg):
        # @TODO add mutex to open_requests object
        RequestsManager.open_requests[request_msg.request_id] = request_msg

    def removeRequest(self,request_id):
        # @TODO add mutex to open_requests object
        del RequestsManager.open_requests[request_id]

    def handleIncomingResponses(self, message):

        # decode message
        # analyze delivery time
        # write output to video stream
        # close request
        pass





