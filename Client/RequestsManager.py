from Utils.Protocols.MQTT.MqttSubscriber import MqttSubscriber
from Utils.Messages.RequestsMessageFactory import RequestsMessageFactory

class RequestsManager:

    # holds requests objects by request_id
    open_requests = {}

    def __init__(self):
        self.listen_flag = False
        self.response_subscriber = None
        self.factory = None
    def initResources(self):
        self.response_subscriber = MqttSubscriber()
        self.factory = RequestsMessageFactory()

    def generateRequest(self,image,algorithm):
        request_msg = self.factory.createRequest(image,algorithm)
        RequestsManager.open_requests[request_msg.request_id] = request_msg
        return request_msg


    def removeRequest(self,request):
        pass

    def handleIncomingResponses(self, message):

        # decode message
        # analyze delivery time
        # write output to video stream
        # close request
        pass





