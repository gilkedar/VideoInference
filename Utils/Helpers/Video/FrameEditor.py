import imutils
import cv2


class FrameEditor:

    def __init__(self):
        pass

    def addTextToFrame(self, frame, text):
        # draw the label on the image
        output = frame
        cv2.putText(output, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        return output

    def addBoxToFrame(self,frame, box, label):
        pass

    def addBoxesToFrame(self, frame, boxes):
        pass
