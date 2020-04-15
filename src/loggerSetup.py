import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] : %(name)s - %(levelname)s - %(message)s')

cnsl_handler = logging.StreamHandler()
cnsl_handler.setLevel(logging.INFO)
cnsl_handler.setFormatter(formatter)

file_handler = logging.FileHandler('FetchData.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

logger.addHandler(cnsl_handler)
logger.addHandler(file_handler)

logger.info("Program Started...")

