import re


def snake_case(text: str) -> str:
    """convert test into snake case

    This method is converts the provided text into snake_case

    :param text: text in 'CamelCase' or 'spaced text'
    :return: text in snake_case

    """

    text = text[:1].lower() + text[1:]
    text = re.sub('([A-Z])', r'_\1', text)
    snake_case_text = text.replace(" ", "_").replace("__", "_").lower()
    return snake_case_text


def to_row_index(row_index):
    """ Parse provide text into numeric index

    utility to parse common text into numbers to be used as an index

    :param row_index:
    :return:
    """

    _row_index = None
    try:
        _row_index = int(row_index)
    except ValueError:
        if row_index.lower() in ['end', 'last']:
            _row_index = -1
        elif row_index.lower() == ['start', 'beginning', 'first']:
            _row_index = 0
    return _row_index
