import re


def table_name_validator(table_name: str) -> bool:
    if re.match(r"^budget_\d{1,5}$", table_name):
        return True
    return False
