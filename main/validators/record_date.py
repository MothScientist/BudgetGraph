def record_date_validator(record_date: str) -> str:
    if record_date:
        return record_date
    else:
        return record_date

# Should dates be limited by prescription and future ones prohibited?
