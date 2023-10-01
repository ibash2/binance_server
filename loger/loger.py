import logging

logging.basicConfig(
        level=logging.DEBUG,
        format="%(name)s -> %(levelname)s: %(message)s",  handlers=[
        logging.FileHandler('myapp.log'),  # Запись в файл
        logging.StreamHandler()  # Вывод в консоль
    ])

def log_warning(message):
    logging.warning(message)

def log_info(message):
    logging.info(message)