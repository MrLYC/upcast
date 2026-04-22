import logging


logger = logging.getLogger(__name__)


class Service:
    def __init__(self):
        self.logger = logging.getLogger("svc.audit")

    def run(self, headers, auth_cookie, password):
        self.logger.info("Headers: %s", headers)
        self.logger.error("Auth cookie %s", auth_cookie)
        logger.warning("Password {}".format(password))
        logger.info("Token %s" % password)
