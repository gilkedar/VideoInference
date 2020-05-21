from imutils.video import VideoStream

class VideoFrameExtractor:

    def __init__(self, source_path=None):
        self.source_path = source_path

        self.current_frame_id = 1
        self.source = None
        self.finished = False

        self.openSource()

    def openSource(self):
        # Read from Driver
        if not self.source_path:
            self.source = VideoStream()
            self.source.start()
        else:
            self.source = VideoStream()  # @Todo - add support to read from file
            self.source.start()

        # vs = VideoStream(src=0).start()

    def closeSource(self):
        self.source.stop()

    def incrementFrameId(self):
        self.current_frame_id += 1

    def getCurrentFrameId(self):
        return self.current_frame_id

    def getNextFrame(self):
        # read frame from driver
        frame = self.source.read()
        frame_id = self.current_frame_id

        if frame is None:
            self.finished = True
        else:
            self.incrementFrameId()

        return frame_id,frame
