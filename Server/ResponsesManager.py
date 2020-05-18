from Utils.Settings import Config
from Utils.Messages.Responses.ResponseMessage import ResponsetMessage
class ResponsesManager:

    # holds requests objects by request_id
    open_requests = {}

    def __init__(self):
        self.requests_publisher = None

    def initResources(self):
        # init response publisher
        pass

    def generateResponseMessage(self,request_id, ans):

        return ResponsetMessage(request_id,ans)

    def add_request(self,request):
        pass

    def removeRequest(self,request):
        pass

    def publishResponse(self,response):
        pass

    def handleIncomingRequests(self,request):

        # decode message
        #
        pass