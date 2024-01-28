CREATE TABLE IF NOT EXISTS Users (
    telegram_id integer PRIMARY KEY NOT NULL UNIQUE,
    username text NOT NULL UNIQUE,
    psw_salt text NOT NULL CHECK(LENGTH(psw_salt) = 32),
    password_hash text NOT NULL CHECK(LENGTH(password_hash) = 64),
    group_id integer NOT NULL,
    last_login text NOT NULL
);

CREATE TABLE IF NOT EXISTS Groups (
    id integer PRIMARY KEY AUTOINCREMENT,
    owner integer NOT NULL UNIQUE, -- telegram_id from Users table
    token text NOT NULL UNIQUE CHECK(LENGTH(token) = 32)
);

CREATE TABLE IF NOT EXISTS UserLanguages (
/*
    Here it is the telegram id, not the user id, since registration is not required to change the language
*/
    telegram_id integer NOT NULL UNIQUE,
    language text NOT NULL CHECK(language IN ('en', 'ru', 'de', 'fr', 'es', 'is'))
);

CREATE TABLE IF NOT EXISTS PremiumUsers (
/*
    Authorization into a premium account occurs via 2FA without a password
*/
    telegram_id integer NOT NULL UNIQUE,
    paid_until text NOT NULL
);