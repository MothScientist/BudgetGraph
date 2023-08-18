# def registration_validator(username: str, password: str, tg_link: str):
#     return True

def registration_validator(username: str, password: str, tg_link: str):
    if len(username) > 2 and len(password) > 2 and len(tg_link) > 2:
        return True
    return False


def token_validator(token: str):
    return True
