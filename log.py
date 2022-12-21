"""Thi module implements basic logger for file and OStream logging"""
import logging


def get_logger():
    """Returns formatted logger"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("log")

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('wins.log')
    c_handler.setLevel(logging.DEBUG)
    c_handler.setLevel(logging.DEBUG)

    c_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    f_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    c_handler.setFormatter(c_formatter)
    f_handler.setFormatter(f_formatter)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger
