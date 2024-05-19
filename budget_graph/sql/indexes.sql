-- Indexes defined when tables are created:
-- CREATE UNIQUE INDEX groups_pkey                  ON budget_graph.groups                  USING btree (id)
-- CREATE UNIQUE INDEX groups_owner_key             ON budget_graph.groups                  USING btree (owner)
-- CREATE UNIQUE INDEX groups_token_key             ON budget_graph.groups                  USING btree (token)
-- CREATE UNIQUE INDEX monetary_transactions_pkey   ON budget_graph.monetary_transactions   USING btree (group_id, transaction_id)
-- CREATE UNIQUE INDEX users_pkey                   ON budget_graph.users                   USING btree (telegram_id)
-- CREATE UNIQUE INDEX users_username_key           ON budget_graph.users                   USING btree (username)
-- CREATE UNIQUE INDEX user_languages_telegram_pkey ON budget_graph.user_languages_telegram USING btree (telegram_id)

-- Creating Indexes
-- to get a list of group users:
CREATE        INDEX IF NOT EXISTS "users_group_id"                       ON "budget_graph"."users"                 USING btree ("group_id");
-- index to check the uniqueness of the username:
CREATE UNIQUE INDEX IF NOT EXISTS "users_lower_username"                 ON "budget_graph"."users"                 USING btree (LOWER("username"));
-- to get a list of group transactions:
CREATE        INDEX IF NOT EXISTS "transactions_group_id"                ON "budget_graph"."monetary_transactions" USING btree ("group_id");
-- index to search for a specific record:
CREATE UNIQUE INDEX IF NOT EXISTS "transactions_transaction_id_group_id" ON "budget_graph"."monetary_transactions" USING btree ("transaction_id" DESC, "group_id");

-- Indexes for analytics
-- to collect group statistics for a certain period:
CREATE INDEX IF NOT EXISTS "transactions_group_id_record_data" ON "budget_graph"."monetary_transactions" USING btree ("group_id", "record_data");
-- to collect user statistics for a certain period:
CREATE INDEX IF NOT EXISTS "transactions_username_record_data" ON "budget_graph"."monetary_transactions" USING btree ("username", "record_data");