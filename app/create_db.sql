CREATE TABLE IF NOT EXISTS groups (
    id    serial      PRIMARY KEY,
    owner bigint      NOT NULL UNIQUE CHECK(owner BETWEEN 1 AND 999999999999),
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