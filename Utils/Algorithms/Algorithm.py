from Utils.Messages.Responses.ImageResponseMessage import ImageResponseMessage
import threading

class Algorithm:

    possible_algorithms = []

    def __init__(self, name, model_path):
        self.name = name
        self.model_path = model_path
        self.model = None
        self.model_lock = threading.Lock()
        self.possible_algorithms.append(self)

    def loadModel(self):
        pass

    def run(self, request_message):
        pass

    def generateResponseMessage(self, input_msg, ans):
        request_id = input_msg.request_id
        serialized_ans = ans.serialize()
        return ImageResponseMessage(request_id=request_id, algorithm=self.name, ans=serialized_ans)
