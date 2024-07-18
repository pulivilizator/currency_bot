import re


def exchange_filter(text: str) -> str:
    pattern = re.compile(r'^[A-Z]{3} [A-Z]{3} \d+[,.]?\d+$')

    # Проверяем соответствие тексту регулярному выражению
    if pattern.match(text):
        return text
    raise ValueError('exchange_error')
