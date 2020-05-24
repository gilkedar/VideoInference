
class ErrorInvalidInputVideoPath(Exception):

    def __init__(self,path):
        self.path = path

    def message(self):
        print("Invalid Video Path Chosen : {}".format(self.path))


class ErrorInvalidInputAlgorithmChoice(Exception):

    def __init__(self, path):
        self.path = path

    def message(self):
        print("Invalid Video Path Chosen : {}".format(self.path))


class ErrorInvalidProtocolChoice(Exception):

    def __init__(self, protocol):
        self.protocol = protocol

    def message(self):
        print("Invalid Protocol Chosen : {}".format(self.protocol))


class ErrorEnvVarNotSet(Exception):

    def __init__(self, param):
        self.param = param

    def message(self):
        print("Missing Environment Variable : {}".format(self.param))
