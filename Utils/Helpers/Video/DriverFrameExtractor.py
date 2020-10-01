from imutils.video import VideoStream
from Utils.Helpers.Video.FrameExtractor import FrameExtractor
from Utils.Exceptions.VideoErrors.VideoErrors import ErrorReadingDriverFrame


class DriverFrameExtractor(FrameExtractor):

    def __init__(self):
        FrameExtractor.__init__(self)
        self.openSource()

    def openSource(self):

        # Read from Driver
        self.source = VideoStream()
        self.source.start()

    def closeSource(self):
        self.source.stop()

    def getNextFrame(self):
        # read frame from driver
        frame = self.source.read()
        if frame is None:
            raise ErrorReadingDriverFrame()
        else:
            self.incrementFrameId()

        frame_id = self.current_frame_id

        # if frame_id == 11:
        #     self.finished = True

        return frame_id, frame
