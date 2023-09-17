import re


def input_number(number: str) -> int | bool:
    number: str = re.sub(r"[^0-9]", "", number)

    if not number or not re.match(r"^(?!0$)(?=.*\d)(?!0\d)\d{0,14}$", number):
        return False
    else:
        return int(number)
