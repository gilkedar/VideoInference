import imutils
import cv2


class FrameEditor:

    def __init__(self):
        pass

    def addFrameIdLabel(self, frame, frame_id):
        output = frame
        cv2.putText(output, "Frame # {}".format(frame_id), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        return output

    def addTextToFrame(self, frame, text):
        # draw the label on the image
        output = frame
        cv2.putText(output, text, (40, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        return output

    def addBoxToFrame(self,frame, box, label):
        pass

    def addBoxesToFrame(self, frame, boxes, lables):

        # TODO - remove box in box ( using small roi)

        for box, label in zip(boxes,lables):
            startX, startY, endX, endY = box
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          (0, 0, 255), 2)
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        return frame

    def encode_to_jpg(self, image):
        (flag, encodedImage) = cv2.imencode(".jpg", image)
        if not flag:
            return None
        return encodedImage
