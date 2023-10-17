import re


def table_name_validator(table_name: str) -> bool:
    """
    Checks if the database name matches the format "budget_N",
    where N is the id of the group to which this database belongs.
    """
    if re.match(r"^budget_[1-9]\d{0,4}$", table_name):
        return True
    return False
