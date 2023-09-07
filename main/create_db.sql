CREATE TABLE IF NOT EXISTS Groups (
    id integer PRIMARY KEY AUTOINCREMENT,
    owner text NOT NULL,
    token text NOT NULL,
);

CREATE TABLE IF NOT EXISTS Users (
    id integer PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL,
    psw_salt text, /*NOT NULL*/
    password_hash text NOT NULL,
    group_id integer NOT NULL,
    telegram_link text NOT NULL,
    last_login real NOT NULL,
);