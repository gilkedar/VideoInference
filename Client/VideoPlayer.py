
class VideoPlayer:

    frames = {}

    def __init__(self,video_path):

        self.file_path = video_path
        self.frame_id = 0
        self.source = None
        self.openSource()
        self.finished = False

    def openSource(self):
        pass

    def getNextFrame(self):
        # read frame from driver
        frame_id = self.frame_id + 1
        frame = None

        # Read from Driver
        if not self.file_path:
            frame = None

        # return next frame from video file
        else:
            frame = None

        VideoPlayer.frames[frame_id] = frame

        if not frame:
            self.finished = True

        return frame

    def viewFrame(self,frame_id):
        pass

    def viewVideoStream(self):
        pass