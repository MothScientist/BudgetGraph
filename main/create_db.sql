CREATE TABLE IF NOT EXISTS Groups (
    id integer PRIMARY KEY AUTOINCREMENT,
    owner text NOT NULL UNIQUE,
    token text NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Users (
    id integer PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL UNIQUE,
    psw_salt text NOT NULL,
    password_hash text NOT NULL,
    group_id integer NOT NULL,
    telegram_link text NOT NULL UNIQUE,
    last_login real NOT NULL
);