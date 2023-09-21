from flask import flash
from database_control import get_db, DatabaseQueries


def login_validator(username: str, psw_hash: str, token: str) -> bool:
    dbase = DatabaseQueries(get_db())
    if dbase.auth_by_username(username, psw_hash, token):
        return True
    flash("This user doesn't exist.", category="error")
    return False
