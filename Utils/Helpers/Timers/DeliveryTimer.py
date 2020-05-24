
from Utils.Helpers.Timers.MessageTimer import MessageTimer


class DeliveryMessageTimer(MessageTimer):

    def __init__(self,message_id, source, destination):
        MessageTimer.__init__(self,message_id)
        self.source = source
        self.destination = destination

    def __str__(self):
        duration = self.start_time - self.end_time
        ms = duration.micorseconds
        return "Duration from {} -> {} : {}".format(self.source,self.destination, ms)
