import logging

def get_logger(log_level=logging.INFO):
    logger = logging.getLogger("uml2dj")
    logger.setLevel(log_level)
    lh = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    lh.setFormatter(formatter)
    logger.addHandler(lh)
    return logger

def logger_adapter(logger, extra):
    class HostAdapter(logging.LoggerAdapter):
        def process(self, msg, kwargs):
            return '%s %s' % (self.extra['host'], msg), kwargs
    return HostAdapter(logger, extra)
