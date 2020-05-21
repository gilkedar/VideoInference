class ErrorReadingDriverFrame(Exception):

    def __init__(self):
        pass

    def message(self):
        print("Error reading frame from source driver")

