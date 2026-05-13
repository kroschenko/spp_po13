# pylint: disable=invalid-name

"""Функция substringBetween для варианта 7."""


def substringBetween(text, open_token, close_token):
    """Возвращает подстроку между открывающей и закрывающей строками."""
    if text is None and open_token is None and close_token is None:
        raise TypeError("All arguments cannot be None")

    if text is None or open_token is None or close_token is None:
        return None

    if open_token == "" and close_token == "":
        return ""

    start = text.find(open_token)

    if start == -1:
        return None

    start += len(open_token)
    end = text.find(close_token, start)

    if end == -1:
        return None

    return text[start:end]
