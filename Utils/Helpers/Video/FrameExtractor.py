
class FrameExtractor:

    def __init__(self):

        self.current_frame_id = 0
        self.source = None
        self.finished = False


    def openSource(self):
        pass

    def closeSource(self):
        pass

    def incrementFrameId(self):
        self.current_frame_id += 1

    def getCurrentFrameId(self):
        return self.current_frame_id

    def getNextFrame(self):
        pass

