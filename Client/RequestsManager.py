from Utils.Messages.RequestsMessageFactory import RequestsMessageFactory
from Utils.Helpers.Video.FrameEditor import FrameEditor
from Utils.Helpers.Video.VideoPlayer import VideoPlayer
from Utils.Infrastructure.DataProtocols.MQTT.MqttDataSubscriber import MqttDataSubscriber
from Utils.Settings import Config

import threading
import time


class RequestsManager:

    # holds requests objects by request_id
    open_requests = {}

    def __init__(self, algorithm, end_condition_variable):

        self.algorithm = algorithm
        self.condition_all_requests_answered = end_condition_variable

        self.listen_flag = False
        self.response_subscriber = None
        self.factory = None
        self.frame_editor = None
        self.video_player = None
        self.end_of_frames = False

        self.requests_lock = threading.Lock()

        self.initResources()

    def initResources(self):
        # Instantiate the factory singleton
        self.factory = RequestsMessageFactory()
        self.frame_editor = FrameEditor()
        self.video_player = VideoPlayer()
        self.initResponseDataSubscriber()

    def initResponseDataSubscriber(self):

        self.response_subscriber = MqttDataSubscriber(Config.MQTT_SERVER_IP, Config.MQTT_TOPIC_NAME, self.handleIncomingResponses)
        # self.response_subscriber = ZmqImageSubscriber(Config.LOCALHOST_IP, self.handleIncomingResponses)
        pass

    def closeResources(self):
        self.response_subscriber = None
        self.factory = None
        self.video_player = None
        self.frame_editor = None

    def startListeningToIncomingResponses(self):
        threading.Thread(target=self.response_subscriber.subscribe).start()
        time.sleep(0.5)  # to stabalize subscriber
        pass

    def getFrame(self,frame_id):
        return RequestsManager.open_requests[frame_id].data

    def generateRequestMessage(self,image_id, image):
        request_msg = self.factory.createImageRequest(image_id, image, self.algorithm)
        self.addRequest(request_msg)
        return request_msg

    def addRequest(self,request_msg):
        with self.requests_lock:
            RequestsManager.open_requests[request_msg.request_id] = request_msg
            print(" + Adding request : {}".format(request_msg.request_id))
    def removeRequest(self,request_id):
        with self.requests_lock:
            del RequestsManager.open_requests[request_id]
            print(" - Removing request : {}".format(request_id))

    def setEndOfFrames(self):
        self.end_of_frames = True

    def notifyEndOfRequests(self):
        with self.condition_all_requests_answered:
            self.condition_all_requests_answered.notify()

    def updateFrameWithResponseData(self, frame_id, response_data):
        if self.algorithm == Config.ALGORITHM_IS_SANTA:
            self.frame_editor.addTextToFrame(frame_id, RequestsManager.open_requests[frame_id],)

    def handleIncomingResponses(self, message):

        # analyze delivery time

        # print output
        print("Response for request id: {} - {}".format(message.request_id, message.ans))

        # close request
        self.removeRequest(message.request_id)
        # check if this was the last request
        if self.end_of_frames and not RequestsManager.open_requests:
            self.notifyEndOfRequests()
        pass





