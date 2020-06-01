import threading
import time

from Utils.Messages.RequestsMessageFactory import RequestsMessageFactory
from Utils.Infrastructure.DataProtocols.MQTT.MqttDataSubscriber import MqttDataSubscriber
from Utils.Helpers.Video.FrameEditor import FrameEditor
from Utils.Helpers.Video.VideoPlayer import VideoPlayer
from Utils.Helpers.TimerManager import TimerManager
from Utils.Helpers.Timers.RequestTimer import RequestMessageTimer
from Utils.Helpers.Logger import Logger
from Utils.Settings import Config

from Utils.Algorithms.AlgorithmResponses.IsSantaResponse import IsSantaResponseMessage


class RequestsManager:

    # holds requests objects by request_id
    open_requests = {}

    def __init__(self, algorithm, end_condition_variable):

        self.algorithm = algorithm
        self.condition_all_requests_answered = end_condition_variable

        self.listen_flag = False
        self.end_of_frames = False

        self.logger = Logger(self.__class__.__name__)
        self.requests_lock = threading.Lock()
        self.timer_manager = TimerManager()
        self.factory = RequestsMessageFactory()
        self.frame_editor = FrameEditor()
        self.video_player = VideoPlayer()

        self.response_subscriber = MqttDataSubscriber(Config.MQTT_SERVER_IP,
                                                      Config.MQTT_TOPIC_NAME,
                                                      self.handleIncomingResponses)

    def closeResources(self):
        self.response_subscriber.stopListening() # @TODO - clean shutdown
        self.timer_manager.printTimers()
        # self.response_subscriber = None
        self.factory = None
        self.video_player = None
        self.frame_editor = None
        
        self.timer_manager = None

    def startListeningToIncomingResponses(self):
        threading.Thread(target=self.response_subscriber.subscribe).start()
        time.sleep(1)  # to stabilize subscriber
        pass

    def getFrame(self,frame_id):
        return RequestsManager.open_requests[frame_id].data

    def generateRequestMessage(self,image_id, image):
        request_msg = self.factory.createImageRequest(image_id, image, self.algorithm)
        return request_msg

    def addRequest(self,request_id, frame):
        with self.requests_lock:
            RequestsManager.open_requests[request_id] = frame
            self.logger.info("Adding request : {}".format(request_id))
            self.timer_manager.startMessageTimer(RequestMessageTimer(request_id))

    def removeRequest(self, request_id):
        with self.requests_lock:
            self.timer_manager.stopMessageTimer(request_id)
            self.logger.info("Removing request : {}".format(request_id))
            del RequestsManager.open_requests[request_id]

    def setEndOfFrames(self):
        self.end_of_frames = True

    def notifyEndOfRequests(self):
        with self.condition_all_requests_answered:
            self.condition_all_requests_answered.notify()

    def updateFrameWithResponseData(self, frame_id, response, original_image):

        if self.algorithm == Config.ALGORITHM_IS_SANTA:
            label = IsSantaResponseMessage.getLabel(frame_id, response)
            return self.frame_editor.addTextToFrame(original_image,label)

    def handleIncomingResponses(self, message):

        # analyze delivery time

        # handle algorithm results - for now just log for testing
        request_id = message.request_id
        ans = message.ans
        self.logger.info("Response for request id: {} - {}".format(request_id, ans))

        original_image = self.open_requests[request_id]
        self.removeRequest(request_id)

        output_frame = self.updateFrameWithResponseData(request_id, ans, original_image)

        self.video_player.viewFrame(output_frame)







