
class TimerManager:

    def __init__(self):

        self.timers = {}

    def startMessageTimer(self, timer):
        self.timers[timer.message_id] = timer
        timer.start()

    def stopMessageTimer(self, message_id):
        timer = self.timers[message_id]
        timer.stop()

    def printTimers(self):
        print("MessageTimers Durations: ({}) Messages".format(len(self.timers)))
        for timer in self.timers.values():
            print(timer)

    def getTimer(self,message_id):
        return self.timers[message_id]