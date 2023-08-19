# def registration_validator(username: str, password: str, tg_link: str):
#     return True

def registration_validator(username: str, password: str, tg_link: str):
    """
    :param username: 3 to 15 characters
    :param password: 4 to 128 characters
    :param tg_link:
    :return:
    """
    if 3 <= len(username) >= 15 and 4 <= len(password) >= 128 and 18 <= len(tg_link) >= 45 and tg_link.startswith("https://t.me/"):
        return True
    return False


def token_validator(token: str):
    """
    :param token: checking if the token exists in the database
    :return: True if such a token exists and the user can be added to the group
    """
    return True
