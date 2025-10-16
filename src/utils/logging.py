import logging


def get_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        ch = logging.StreamHandler()
        fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")
        ch.setFormatter(fmt)
        logger.addHandler(ch)
    return logger
