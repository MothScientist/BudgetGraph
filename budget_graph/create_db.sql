-- Create a schema:
CREATE SCHEMA IF NOT EXISTS "budget_graph";

-- Creating tables:
CREATE TABLE IF NOT EXISTS "budget_graph"."groups" (
    "id"    serial      PRIMARY KEY,
    "owner" bigint      NOT NULL UNIQUE CHECK("owner" > 0 AND "owner" < 1000000000000),
    "token" varchar(32) NOT NULL UNIQUE CHECK(LENGTH("token") = 32)
);
CREATE TABLE IF NOT EXISTS "budget_graph"."users" (
    "telegram_id"  bigint       NOT NULL          CHECK("telegram_id" > 0 AND "telegram_id" < 1000000000000),
    "username"     varchar(20)  NOT NULL  UNIQUE  CHECK(LENGTH("username") >= 3),
    "psw_salt"     varchar(32)  NOT NULL          CHECK(LENGTH("psw_salt") = 32),
    "psw_hash"     varchar(64)  NOT NULL          CHECK(LENGTH("psw_hash") = 64),
    "group_id"     integer      NOT NULL          CHECK("group_id" > 0), -- индекс по группе
    "last_login"   varchar(19),  -- (сделать NULL по дефолту!) NULL пригодится для скрытия времени для премиум юзеров + добавить CHECK что либо NULL, либо не ранее даты создания таблицы
    PRIMARY KEY    ("telegram_id") -- last_login переделать на тип поля date (как в monetary_transactions в поле record_date) - мб стоит перейти на UTC
);
CREATE TABLE IF NOT EXISTS "budget_graph"."monetary_transactions" (
    "group_id"       integer      NOT NULL  CHECK("group_id" > 0), -- индекс (отдельный)
    "transaction_id" integer      NOT NULL  CHECK("transaction_id" > 0),
    "username"       varchar(20)  NOT NULL  CHECK(LENGTH("username") >= 3),
    "total"          integer      NOT NULL,
    "transfer"       integer      NOT NULL,
    "record_date"    date         NOT NULL, -- тут тоже индекс, чтобы брать аналитику по срезам дат
    "category"       varchar(25)  NOT NULL, -- индекс (group_id, category) - пригодится для аналитики
    "description"    varchar(50)  NOT NULL,
    PRIMARY KEY ("group_id", "transaction_id")
);
CREATE TABLE IF NOT EXISTS "budget_graph"."user_languages_telegram" (
    "telegram_id"  bigint       NOT NULL  UNIQUE  CHECK("telegram_id" > 0 AND "telegram_id" < 1000000000000),
    "language"     varchar(2)   NOT NULL          CHECK("language" IN ('en', 'ru', 'de', 'fr', 'es', 'is')),
    PRIMARY KEY    ("telegram_id")
);
CREATE TABLE IF NOT EXISTS "budget_graph"."premium_groups" (
    "id"             serial       PRIMARY KEY,
    "paid_until"     date         NOT NULL,
    "premium_status" boolean      NOT NULL,
    "owner"          bigint       NOT NULL  UNIQUE  CHECK("owner" > 0),
    "token"          varchar(16)  NOT NULL  UNIQUE  CHECK(LENGTH("token") = 16),
    "user_limit"     smallint                       CHECK("user_limit" > 0)
);
CREATE TABLE IF NOT EXISTS "budget_graph"."premium_users" (
    "telegram_id" bigint   NOT NULL CHECK("telegram_id" > 0 AND "telegram_id" < 1000000000000),
    "group_id"    integer  NOT NULL CHECK("group_id" > 0),
    PRIMARY KEY   ("telegram_id")
    -- FOREIGN KEY (group_id) REFERENCES "premium_groups"."id"
);

-- Automatic indexes:
-- CREATE UNIQUE INDEX groups_pkey ON budget_graph.groups USING btree (id)
-- CREATE UNIQUE INDEX groups_owner_key ON budget_graph.groups USING btree (owner)
-- CREATE UNIQUE INDEX groups_token_key ON budget_graph.groups USING btree (token)
-- CREATE UNIQUE INDEX monetary_transactions_pkey ON budget_graph.monetary_transactions USING btree (group_id, transaction_id)
-- CREATE UNIQUE INDEX users_pkey ON budget_graph.users USING btree (telegram_id)
-- CREATE UNIQUE INDEX users_username_key ON budget_graph.users USING btree (username)
-- CREATE UNIQUE INDEX user_languages_telegram_pkey ON budget_graph.user_languages_telegram USING btree (telegram_id)

-- Creating Indexes:
CREATE INDEX IF NOT EXISTS "users_group_id" ON "budget_graph"."users" USING btree ("group_id");
CREATE UNIQUE INDEX IF NOT EXISTS "users_lower_username" ON "budget_graph"."users" USING btree (LOWER("username"));
CREATE INDEX IF NOT EXISTS "monetary_transactions_group_id" ON "budget_graph"."monetary_transactions" USING btree ("group_id");
CREATE UNIQUE INDEX IF NOT EXISTS "monetary_transactions_group_id_transaction_id" ON "budget_graph"."monetary_transactions" USING btree ("group_id", "transaction_id" DESC);

