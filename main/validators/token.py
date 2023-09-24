from database_control import get_db, DatabaseQueries, connect_db, close_db_main


def token_validator(token: str) -> int:
    """
    :param token: checking if the token exists in the database
    :return: 0 - if there is no group with this token
             x - if the group exists (x - group id)
    """
    connection = connect_db()
    dbase = DatabaseQueries(connection)
    group_id = dbase.get_group_id_by_token(token)
    close_db_main(connection)
    return group_id
