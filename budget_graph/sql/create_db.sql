-- Setting up the date format to eliminate errors when converting ::date
ALTER DATABASE postgres SET datestyle TO 'iso, dmy';

-- Create a schema:
CREATE SCHEMA IF NOT EXISTS "budget_graph";

-- Creating tables:
CREATE TABLE IF NOT EXISTS "budget_graph"."users" (
    "telegram_id" bigint                   PRIMARY KEY        CHECK("telegram_id" BETWEEN 1 AND POWER(10, 12) - 1),
    "username"    varchar(20)              NOT NULL    UNIQUE CHECK(LENGTH("username") BETWEEN 3 AND 20),
    "psw_salt"    varchar(32)              NOT NULL           CHECK(LENGTH("psw_salt") = 32),
    "psw_hash"    varchar(64)              NOT NULL           CHECK(LENGTH("psw_hash") = 64),
    "last_login"  timestamp with time zone     NULL,
    -- user time zone
    "timezone"    smallint                     NULL           CHECK("timezone" IS NULL OR "timezone" >= -12 AND "timezone" <= 12),
    -- other settings for the user (for example, the activation status of some functionality)
    -- 0: Status that the dialog clearing function is enabled after a successful transaction
    -- 1: Reserve
    -- 2: Reserve
    -- 3: Reserve
    -- 4: Reserve
    -- 5: Reserve
    -- 6: Reserve
    -- 7: Reserve
    -- 8: Reserve
    -- 9: Reserve
    "settings"    boolean[]
                  DEFAULT ARRAY[NULL::bool, NULL::bool,
                                NULL::bool, NULL::bool,
                                NULL::bool, NULL::bool,
                                NULL::bool, NULL::bool,
                                NULL::bool, NULL::bool]       CHECK(array_length("settings", 1) = 10)
);
CREATE TABLE IF NOT EXISTS "budget_graph"."groups" (
    "id"           smallserial PRIMARY KEY, -- It makes sense to add a UNIQUE or PRIMARY KEY constraint on this
                                            -- column to protect against erroneously adding duplicate values,
                                            -- but this does not happen automatically
    "owner"        bigint      NOT NULL UNIQUE    CHECK("owner" BETWEEN 1 AND POWER(10, 12) - 1),
    "token"        varchar(32) NOT NULL UNIQUE    CHECK(LENGTH("token") = 32),
    -- number of participants in the group (auto filling and counting)
    "users_number" smallint    NOT NULL DEFAULT 1 CHECK(("users_number" BETWEEN 1 AND 20) OR "users_number" IS NULL)
);
CREATE TABLE IF NOT EXISTS "budget_graph"."users_groups" (
    "telegram_id" bigint          PRIMARY KEY CHECK("telegram_id" BETWEEN 1 AND POWER(10, 12) - 1),
    "group_id"    smallint        NOT NULL    CHECK("group_id" > 0)
);
CREATE TABLE IF NOT EXISTS "budget_graph"."monetary_transactions" (
    "group_id"       smallint    NOT NULL CHECK("group_id" > 0),
    "transaction_id" integer     NOT NULL CHECK("transaction_id" > 0),
    "username"       varchar(20) NOT NULL CHECK(LENGTH("username") BETWEEN 3 AND 20),
    "total"          integer     NOT NULL,
    "transfer"       integer     NOT NULL CHECK("transfer" <> 0),
    "record_date"    date        NOT NULL,
    "category"       varchar(25)     NULL,
    "description"    varchar(50)     NULL,
    PRIMARY KEY      ("group_id", "transaction_id")
);
CREATE TABLE IF NOT EXISTS "budget_graph"."user_languages_telegram" (
    "telegram_id"  bigint     NOT NULL UNIQUE CHECK("telegram_id" BETWEEN 1 AND POWER(10, 12) - 1),
    "language"     varchar(2) NOT NULL        CHECK("language" IN ('en', 'ru', 'de', 'fr', 'es', 'is', 'kk', 'pt')),
    PRIMARY KEY    ("telegram_id")
);
CREATE TABLE IF NOT EXISTS "budget_graph"."premium_users" (
    "telegram_id"    bigint  NOT NULL CHECK("telegram_id" BETWEEN 1 AND POWER(10, 12) - 1),
    "paid_until"     date    NOT NULL,
    "premium_status" boolean NOT NULL DEFAULT False, -- auto fill depending on "paid_until"
    PRIMARY KEY      ("telegram_id")
);