-- Create a schema:
CREATE SCHEMA IF NOT EXISTS "budget_graph";

-- Creating tables:
CREATE TABLE IF NOT EXISTS "budget_graph"."groups" (
    "id"    smallserial        PRIMARY KEY, -- It makes sense to add a UNIQUE or PRIMARY KEY constraint on this
                                            -- column to protect against erroneously adding duplicate values,
                                            -- but this does not happen automatically
    "owner"        bigint      NOT NULL UNIQUE CHECK("owner" BETWEEN 1 AND POWER(10, 12) - 1),
    "token"        varchar(32) NOT NULL UNIQUE CHECK(LENGTH("token") = 32),
    -- number of participants in the group (auto filling and counting)
    "users_number" smallint        NULL        CHECK(("users_number" BETWEEN 1 AND 20) OR "users_number" IS NULL)
);
CREATE TABLE IF NOT EXISTS "budget_graph"."users" (
    "telegram_id" bigint      PRIMARY KEY        CHECK("telegram_id" BETWEEN 1 AND POWER(10, 12) - 1),
    "username"    varchar(20) NOT NULL    UNIQUE CHECK(LENGTH("username") BETWEEN 3 AND 20),
    "psw_salt"    varchar(32) NOT NULL           CHECK(LENGTH("psw_salt") = 32),
    "psw_hash"    varchar(64) NOT NULL           CHECK(LENGTH("psw_hash") = 64),
    "group_id"    integer     NOT NULL           CHECK("group_id" > 0), -- индекс по группе
    "last_login"  varchar(19)     NULL  -- переделать на тип date (как в monetary_transactions в поле record_date)
);
CREATE TABLE IF NOT EXISTS "budget_graph"."monetary_transactions" (
    "group_id"       smallint    NOT NULL CHECK("group_id" > 0), -- индекс (отдельный)
    "transaction_id" integer     NOT NULL CHECK("transaction_id" > 0),
    "username"       varchar(20) NOT NULL CHECK(LENGTH("username") BETWEEN 3 AND 20),
    "total"          integer     NOT NULL,
    "transfer"       integer     NOT NULL  CHECK("transfer" <> 0),
    "record_date"    date        NOT NULL, -- (group_id, record_date) индекс, чтобы брать аналитику по срезам дат
    "category"       varchar(25)     NULL, -- индекс (group_id, category) + (username, category) + (record_date, category) - пригодится для аналитики -> добавить NULL в БЛ
    "description"    varchar(50)     NULL, -- -> добавить NULL в БЛ
    PRIMARY KEY ("group_id", "transaction_id")
);
CREATE TABLE IF NOT EXISTS "budget_graph"."user_languages_telegram" (
    "telegram_id"  bigint     NOT NULL UNIQUE CHECK("telegram_id" BETWEEN 1 AND POWER(10, 12) - 1),
    "language"     varchar(2) NOT NULL        CHECK("language" IN ('en', 'ru', 'de', 'fr', 'es', 'is', 'kk', 'pt')),
    PRIMARY KEY    ("telegram_id")
);
CREATE TABLE IF NOT EXISTS "budget_graph"."premium_users" (
    "telegram_id" bigint  NOT NULL CHECK("telegram_id" BETWEEN 1 AND POWER(10, 12) - 1),
    "group_id"    integer NOT NULL CHECK("group_id" > 0),
    PRIMARY KEY   ("telegram_id")
    -- FOREIGN KEY (group_id) REFERENCES "premium_groups"."id"
);