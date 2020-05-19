from Utils.Infrastructure.Publisher import Publisher


class DataPublisher(Publisher):

    def __init__(self, protocol):
        Publisher.__init__(self, protocol)

    def publish(self, message):
        pass
