from Utils.Messages.Responses.ImageResponseMessage import ImageResponseMessage


class Algorithm:

    possible_algorithms = []

    def __init__(self, name, model_path):
        self.name = name
        self.model_path = model_path

        self.possible_algorithms.append(self)

    def loadModel(self):
        pass

    def run(self, model_input):
        pass

    def generateResponseMessage(self, input_msg, ans):
        request_id = input_msg.request_id
        return ImageResponseMessage(request_id=request_id, algorithm=self.name, ans=ans)
