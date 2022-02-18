import logging


def get_logger(logger_name: str, logging_level='INFO'):
    """
    Returns logger that outputs to standard out
            Parameters:
                logger_name (str): Name of logger
                logging_level (str): A logging level

            Returns:
                logger (logging.Logger): A logger instance
    """
    logger = logging.getLogger(logger_name)
    handler = logging.StreamHandler()
    logger.setLevel(logging_level)
    handler.setLevel(logging_level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
