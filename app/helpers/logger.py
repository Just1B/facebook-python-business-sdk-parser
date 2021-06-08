import logging


def get_app_logger(mod_name):
    """
        Custom logger method
        To use this, do logger = get_module_logger(__name__)
    """

    formatter = logging.Formatter(
        "%(asctime)s [ %(name)s ] %(levelname)-3s : %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(mod_name)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(handler)

    return logger


class LoggerMixin(object):
    @property
    def logger(self):
        return get_app_logger(self.__class__.__name__)
