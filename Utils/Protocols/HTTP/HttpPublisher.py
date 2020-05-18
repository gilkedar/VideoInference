import socket
from Utils.Settings import Config

class HttpPublisher:

    def __init__(self, ip, port=Config.HTTP_DEFAULT_PORT):
        self.ip = ip
        self.port = port

        # self.sender = imagezmq.ImageSender(connect_to="tcp://{}:{}}".format(ip, port), REQ_REP=False)

    def publish(self,message):

        rpi_name = socket.gethostname()  # send RPi hostname with each image
        # self.sender.send_image(rpi_name, image)
