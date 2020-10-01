from Utils.Messages.Responses.ImageResponseMessage import ImageResponseMessage
from Utils.Helpers.Video.FrameEditor import FrameEditor
import threading


class Algorithm:

    possible_algorithms = []

    def __init__(self, name, model_path):
        self.name = name
        self.model_path = model_path
        self.model = None
        self.model_lock = threading.Lock()
        self.frame_editor = FrameEditor()
        self.possible_algorithms.append(self)

    def loadModel(self):
        pass

    def preProcessData(self, original_frame):
        pass

    def run(self, input_msg):
        pass

    def updateFrame(self, original_frame, response):
        pass

    def generateResponseMessage(self, request_message, ans):
        request_id = request_message.request_id
        serialized_ans = ans.serialize()
        original_frame = request_message.data
        updated_frame = self.updateFrame(original_frame, ans)
        return ImageResponseMessage(request_id=request_id, algorithm=self.name, ans=serialized_ans, updated_frame=updated_frame)
