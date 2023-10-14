CREATE TABLE IF NOT EXISTS Groups (
    id integer PRIMARY KEY AUTOINCREMENT,
    owner integer NOT NULL UNIQUE,
    token text NOT NULL UNIQUE CHECK(LENGTH(token) = 32)
);

CREATE TABLE IF NOT EXISTS Users (
    id integer PRIMARY KEY AUTOINCREMENT,
    username text NOT NULL UNIQUE,
    psw_salt text NOT NULL CHECK(LENGTH(psw_salt) = 32),
    password_hash text NOT NULL CHECK(LENGTH(password_hash) = 64),
    group_id integer NOT NULL,
    telegram_id integer NOT NULL UNIQUE,
    last_login real NOT NULL,
    is_premium integer NOT NULL CHECK (is_premium IN (0, 1))
);