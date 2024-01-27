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
    owner integer NOT NULL UNIQUE,
    token text NOT NULL UNIQUE CHECK(LENGTH(token) = 32)
);

CREATE TABLE IF NOT EXISTS UserLanguages (
    telegram_id integer NOT NULL UNIQUE,
    language text NOT NULL CHECK(language IN ('en', 'ru', 'de', 'fr', 'es', 'is'))
);

CREATE TABLE IF NOT EXISTS PremiumUsers (
    telegram_id integer NOT NULL UNIQUE,
    paid_until text NOT NULL
);

CREATE TABLE IF NOT EXISTS budget_1 (
    id integer PRIMARY KEY AUTOINCREMENT,
    total integer NOT NULL,
    username text NOT NULL,
    transfer integer NOT NULL,
    category text NOT NULL,
    record_date text NOT NULL,
    description text CHECK(LENGTH(description) <= 50)
);

CREATE TABLE IF NOT EXISTS budget_2 (
    id integer PRIMARY KEY AUTOINCREMENT,
    total integer NOT NULL,
    username text NOT NULL,
    transfer integer NOT NULL,
    category text NOT NULL,
    record_date text NOT NULL,
    description text CHECK(LENGTH(description) <= 50)
);

CREATE TABLE IF NOT EXISTS budget_3 (
    id integer PRIMARY KEY AUTOINCREMENT,
    total integer NOT NULL,
    username text NOT NULL,
    transfer integer NOT NULL,
    category text NOT NULL,
    record_date text NOT NULL,
    description text CHECK(LENGTH(description) <= 50)
);

CREATE TABLE IF NOT EXISTS budget_10 (
    id integer PRIMARY KEY AUTOINCREMENT,
    total integer NOT NULL,
    username text NOT NULL,
    transfer integer NOT NULL,
    category text NOT NULL,
    record_date text NOT NULL,
    description text CHECK(LENGTH(description) <= 50)
);

INSERT INTO Groups (owner, token)
VALUES ('123456780', '3cf060bde115a4b3a3c29e7459150673');

INSERT INTO Groups (owner, token)
VALUES ('1234561', 'e00a6e6d1d1a54b017d5fa348534b7e8');

INSERT INTO Groups (owner, token)
VALUES ('2222222', '3fdf370474a3a0e4008499c44a420f8e');

INSERT INTO Groups (id, owner, token)
VALUES (10, '1111111', '3c376424479c9a92649721e23ff9cc9b');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Alex_Alex12345', '71Zwm1hvnlyD7eQUJK0RlfOBqF3lYhYY', 'c20b735096a231a491d94fe15de5cfefd181c82ae8cef38f3abb9174feddf98d', 1, 123456780, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Thomas_Thomas1', 'eFrt7GqNHlFHLMbmcE2U8Fc1x0ysMMQJ', '42ac2f592de057b3384158fdfe05e18dda61f686f03fbf1b61f71dd2d4a377bb', 1, 123456781, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Juliette_Juliette2', 'cLZZfzclKmw4hKwQN5MNHr9jQjQbWCX4', '52279909441af52e377302c896f5596b94faf4234b70f92cf7e0c0ddbf97caca', 1, 123456782, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Alexandre_Alexandre0', 'Q9biK0IFensNyzicpHJQTbUXKqaGEfzA', 'eb03b0d84ef676645760add6b84eecebdbefeac61e14e736901db008b55ab7bd', 1, 123456783, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Hugo', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456799, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Marco', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456798, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Francesca', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456797, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Giovanni', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456796, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Isabella', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456795, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Giorgio', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456794, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Valentina', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456793, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Lorenzo', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456792, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Elena', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456791, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Vincenzo', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456790, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Bianca', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456789, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Carter', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456788, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Stella', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456787, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Jackson', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456786, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Aria', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456785, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Olivier', 'NiWfL76NRWx3hmLBQMJkhkIfRwWGHZ0U', '7755b9530886bf1468005c6ef04a1fa7f0516a7e224491efac91b19e4c72b87c', 1, 123456784, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Grayson', 'Shvugemj43TFPcnyIQ4MWPnKhdo7q3Ee', 'd65d87a2833d1ac0f159b6b5b3fa70ad5d0f369db786b0ed9fceb853ab703e1c', 2, 1234561, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Alessandro', 'Shvugemj43TFPcnyIQ4MWPnKhdo7q3Ee', 'd65d87a2833d1ac0f159b6b5b3fa70ad5d0f369db786b0ed9fceb853ab703e1c', 2, 1234562, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Nathan', 'Shvugemj43TFPcnyIQ4MWPnKhdo7q3Ee', 'd65d87a2833d1ac0f159b6b5b3fa70ad5d0f369db786b0ed9fceb853ab703e1c', 2, 1234563, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Lincoln', '2hsGtWb6x2U1R9ci4ZSXjF5EpRxV9KxN', '65c70178e16b2fb28667f10fdab320fc128e0dc71bf1f5725e29e145972e0cdd', 3, 2222222, '01/10/2023');

INSERT INTO Users (username, psw_salt, password_hash, group_id, telegram_id, last_login)
VALUES ('Kennedy', 'NFqP8q7QrCZbBv6X4vfzf5Wxu3pjTU3T', '9aa93aa6aeb222653c3deb2f5e6e004db066a972cb2a08b7038926fd45f99f05', 10, 1111111, '01/10/2023');

INSERT INTO budget_1 (total, username, transfer, category, record_date)
VALUES (500, 'Hugo', 500, 'Other', '15/06/2021');

INSERT INTO budget_1 (total, username, transfer, category, record_date)
VALUES (0, 'Hugo', -500, 'Other', '15/06/2021');

INSERT INTO budget_1 (total, username, transfer, category, record_date)
VALUES (5000, 'Hugo', 5000, 'Other', '15/06/2021');

INSERT INTO budget_1 (total, username, transfer, category, record_date)
VALUES (37500, 'Hugo', 32500, 'Other', '15/06/2021');

INSERT INTO budget_2 (total, username, transfer, category, record_date)
VALUES (120000, 'Alessandro', 120000, 'Other', '01/01/2021');

INSERT INTO budget_2 (total, username, transfer, category, record_date)
VALUES (240000, 'Alessandro', 120000, 'Other', '01/01/2021');

INSERT INTO budget_2 (total, username, transfer, category, record_date)
VALUES (0, 'Alessandro', -240000, 'Other', '01/01/2021');

-- Table budget_10 is empty

INSERT INTO UserLanguages (telegram_id, language)
VALUES (123456783, 'en');

INSERT INTO UserLanguages (telegram_id, language)
VALUES (123456780, 'ru');

INSERT INTO UserLanguages (telegram_id, language)
VALUES (123456793, 'es');

INSERT INTO UserLanguages (telegram_id, language)
VALUES (123456786, 'is');

INSERT INTO UserLanguages (telegram_id, language)
VALUES (1234563, 'de');
