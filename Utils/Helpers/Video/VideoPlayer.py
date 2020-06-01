import time
import cv2


class VideoPlayer:

    def __init__(self,):
        pass

    def viewFrame(self,frame):

        cv2.imshow("VideoInference)", frame)

        cv2.waitKey(0)

    def playFrames(self, frames):
        pass
