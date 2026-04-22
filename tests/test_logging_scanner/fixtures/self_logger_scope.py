import logging


class ServiceA:
    def __init__(self):
        self.logger = logging.getLogger("svc.alpha")

    def run(self):
        self.logger.info("alpha message")


class ServiceB:
    def __init__(self):
        self.logger = logging.getLogger("svc.beta")

    def run(self):
        self.logger.info("beta message")
