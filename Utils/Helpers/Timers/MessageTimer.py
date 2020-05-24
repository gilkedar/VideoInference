import time

class MessageTimer:

    def __init__(self, message_id):
        self.message_id = message_id
        self.start_time = None
        self.end_time = None
        self.duration = 0

    @staticmethod
    def get_curr_time():
        return time.perf_counter()

    def start(self):
        self.start_time = self.get_curr_time()

    def stop(self):
        self.end_time = self.get_curr_time()

    def getDuration(self):
        return self.end_time - self.start_time

    def __str__(self):
        duration = self.getDuration()
        return " {} : {:.3f} seconds".format(self.message_id, duration)
