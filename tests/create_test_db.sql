CREATE TABLE IF NOT EXISTS groups (
    id    serial      PRIMARY KEY,
    owner bigint      NOT NULL UNIQUE CHECK(telegram_id BETWEEN 1 AND 999999999999),
    token varchar(32) NOT NULL UNIQUE CHECK(LENGTH(token) = 32)
);

CREATE TABLE IF NOT EXISTS users (
    telegram_id bigint      NOT NULL        CHECK(telegram_id BETWEEN 1 AND 999999999999),
    username    varchar(20) NOT NULL UNIQUE CHECK(LENGTH(username) >= 3),
    psw_salt    varchar(32) NOT NULL        CHECK(LENGTH(psw_salt) = 32),
    psw_hash    varchar(64) NOT NULL        CHECK(LENGTH(psw_hash) = 64),
    group_id    integer     NOT NULL        CHECK(group_id > 0),
    last_login  varchar(19) NOT NULL,
    PRIMARY KEY (telegram_id)
);

CREATE TABLE IF NOT EXISTS monetary_transactions (
    group_id       integer     NOT NULL  CHECK(group_id > 0),
    transaction_id integer     NOT NULL  CHECK(transaction_id > 0),
    username       varchar(20) NOT NULL  CHECK(LENGTH(username) >= 3),
    total          integer     NOT NULL,
    transfer       integer     NOT NULL,
    record_date    date        NOT NULL,
    category       varchar(25) NOT NULL,
    description    varchar(50) NOT NULL,
    PRIMARY KEY (group_id, transaction_id)
);

CREATE TABLE IF NOT EXISTS user_languages_telegram (
    telegram_id bigint     NOT NULL CHECK(telegram_id BETWEEN 1 AND 999999999999),
    language    varchar(2) NOT NULL CHECK(language IN ('en', 'ru', 'de', 'fr', 'es', 'is')),
    PRIMARY KEY (telegram_id)
);

CREATE TABLE IF NOT EXISTS premium_groups (
    id             serial      PRIMARY KEY,
    paid_until     date        NOT NULL,
    premium_status boolean     NOT NULL,
    owner          bigint      NOT NULL UNIQUE CHECK(owner > 0),
    token          varchar(16) NOT NULL UNIQUE CHECK(LENGTH(token) = 16),
    user_limit     smallint                    CHECK(user_limit > 0)
);

CREATE TABLE IF NOT EXISTS premium_users (
    telegram_id bigint  NOT NULL CHECK(telegram_id > 0),
    group_id    integer NOT NULL CHECK(group_id > 0),
    PRIMARY KEY (telegram_id),
    FOREIGN KEY (group_id) REFERENCES premium_groups(id)
);


INSERT INTO groups (id, owner, token)
VALUES (1, 104500, '1522ec5ff608a6d1d52e56bfa205666c');

INSERT INTO groups (id, owner, token)
VALUES (2, 43251001, '4069ca3e7b5c0fc1cf8101764e1ee468');

INSERT INTO groups (id, owner, token)
VALUES (3, 5236002, '28b670e597ab8ba047c2009bea2e093b');

INSERT INTO groups (id, owner, token)
VALUES (4, 3242003, 'cf58916a5ff94010fe2308255c060da0');

INSERT INTO groups (id, owner, token)
VALUES (5, 3430004, 'cd8bbf16d323e2eaf38d8be9232784de');

INSERT INTO groups (id, owner, token)
VALUES (6, 5345005, '0f05dc849d0fa05cf75b96a406b90f50');

INSERT INTO groups (id, owner, token)
VALUES (7, 2345456, '0f6d4b6d1be3ef50dd3759e9e589c82b');

INSERT INTO groups (id, owner, token)
VALUES (8, 1254557, '33cc7e17d399b5bf51225ef74fd49d61');

INSERT INTO groups (id, owner, token)
VALUES (9, 1131538, '936ac0c10704f0dd8fb4fe465644b90a');

INSERT INTO groups (id, owner, token)
VALUES (10, 2462609, 'dbc3731b827a12f9564d73540cb230cb');

INSERT INTO users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
VALUES (104500, 'User1', '', '', 1, '');

INSERT INTO users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
VALUES (43251001, 'User2', '', '', 2, '');

INSERT INTO users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
VALUES (5236002, 'User3', '', '', 3, '');

INSERT INTO users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
VALUES (3242003, 'User4', '', '', 4, '');

INSERT INTO users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
VALUES (3430004, 'User5', '', '', 5, '');

INSERT INTO users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
VALUES (5345005, 'User6', '', '', 6, '');

INSERT INTO users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
VALUES (2345456, 'User7', '', '', 7, '');

INSERT INTO users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
VALUES (1254557, 'User8', '', '', 8, '');

INSERT INTO users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
VALUES (1131538, 'User9', '', '', 9, '');

INSERT INTO users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
VALUES (2462609, 'User10', '', '', 10, '');

INSERT INTO user_languages_telegram (telegram_id, language)
VALUES (104500, 'en');

INSERT INTO user_languages_telegram (telegram_id, language)
VALUES (2462609, 'en');

INSERT INTO user_languages_telegram (telegram_id, language)
VALUES (43251001, 'ru');

INSERT INTO user_languages_telegram (telegram_id, language)
VALUES (3242003, 'es');

INSERT INTO user_languages_telegram (telegram_id, language)
VALUES (5345005, 'is');

INSERT INTO user_languages_telegram (telegram_id, language)
VALUES (1254557, 'de');
