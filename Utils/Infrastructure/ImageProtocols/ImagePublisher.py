from Utils.Infrastructure.Publisher import Publisher


class ImagePublisher(Publisher):

    def __init__(self, protocol):
        Publisher.__init__(self,protocol)

    def publish(self, message):
        pass
