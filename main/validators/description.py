def description_validation(description: str) -> bool:
    if len(description) <= 50:
        return True
    else:
        return False
