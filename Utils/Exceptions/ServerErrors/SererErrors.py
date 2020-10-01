
class ErrorInvalidAlgorithm(Exception):

    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.message = "Invalid Algorithm  : {}".format(self.algorithm)
