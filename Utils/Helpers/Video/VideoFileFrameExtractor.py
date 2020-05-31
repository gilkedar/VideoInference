import cv2

from Utils.Helpers.Video.FrameExtractor import FrameExtractor


class VideoFileFrameExtractor(FrameExtractor):

    supported_formats = ["mp4", "mkv"]  # @TODO - test other formates and raise errors

    def __init__(self, file_path):
        FrameExtractor.__init__(self)
        self.file_path = file_path
        self.openSource()

    def openSource(self):
        self.source = cv2.VideoCapture(self.file_path)

    def closeSource(self):
        self.source.release()

    def getNextFrame(self):
        success, frame = self.source.read()
        if not success:
            self.finished = True
            frame = None
        else:
            self.incrementFrameId()

        frame_id = self.current_frame_id

        if frame_id == 11:
            self.finished = True

        return frame_id, frame


