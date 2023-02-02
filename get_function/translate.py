import translators as ts
from loguru import logger


def get_your_translate(user_input):
    logger.info(f'User use the function get_your_translate')
    return ts.translate_text(user_input, to_language='ru')
