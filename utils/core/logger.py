import logging
import os

def setup_logger(name='default_logger', log_file='logs/logs.log', level=logging.INFO):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        '[%(asctime)s.%(msecs)-3d] %(filename)s:%(lineno)d #%(levelname)s - %(message)s',
        datefmt='%H:%M:%S %d/%m/%y'
    )

    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

logger = setup_logger('bybit_logger')

logger.info("Информация о логировании.")

