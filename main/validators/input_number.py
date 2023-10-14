import re


def input_number(number: str) -> int:
    """
    Validation of a number that can be misspelled as characters within a string.
    For example, 10a00 -> 1000
    :param number: Number as a string value.
    :return: Returns int(number) if validation passed, returns 0 (False) if validation failed.
    """
    number: str = re.sub(r"[^0-9]", "", number)

    if not number or not re.match(r"^(?!0$)(?=.*\d)(?!0\d)\d{0,14}$", number):
        return 0
    else:
        return int(number)


if __name__ == '__main__':
    pass
