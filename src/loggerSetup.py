import logging

def get_logger(moduleName, logFilePath):

    logger = logging.getLogger(moduleName)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] : %(name)s - %(levelname)s - %(message)s')

    cnsl_handler = logging.StreamHandler()
    cnsl_handler.setLevel(logging.INFO)
    cnsl_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(logFilePath)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(cnsl_handler)
    logger.addHandler(file_handler)

    return logger
