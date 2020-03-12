class Logger(object):
    def __init__(self):
        print("inited")
        self.counter = 0

    def increment(self):
        self.counter += 1
        print(self.counter)


logger = Logger()


def increment_counter():
    logger.increment()

