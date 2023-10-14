def description_validator(description: str) -> bool:
    if len(description) <= 50:
        return True
    else:
        return False
