-- Automatic indexes:
-- CREATE UNIQUE INDEX groups_pkey ON budget_graph.groups USING btree (id)
-- CREATE UNIQUE INDEX groups_owner_key ON budget_graph.groups USING btree (owner)
-- CREATE UNIQUE INDEX groups_token_key ON budget_graph.groups USING btree (token)
-- CREATE UNIQUE INDEX monetary_transactions_pkey ON budget_graph.monetary_transactions USING btree (group_id, transaction_id)
-- CREATE UNIQUE INDEX users_pkey ON budget_graph.users USING btree (telegram_id)
-- CREATE UNIQUE INDEX users_username_key ON budget_graph.users USING btree (username)
-- CREATE UNIQUE INDEX user_languages_telegram_pkey ON budget_graph.user_languages_telegram USING btree (telegram_id)

-- Creating Indexes:
CREATE         INDEX  IF NOT EXISTS  "users_group_id"                                 ON "budget_graph"."users"                 USING btree  ("group_id");
CREATE UNIQUE  INDEX  IF NOT EXISTS  "users_lower_username"                           ON "budget_graph"."users"                 USING btree  (LOWER("username"));
CREATE         INDEX  IF NOT EXISTS  "monetary_transactions_group_id"                 ON "budget_graph"."monetary_transactions" USING btree  ("group_id");
CREATE UNIQUE  INDEX  IF NOT EXISTS  "monetary_transactions_group_id_transaction_id"  ON "budget_graph"."monetary_transactions" USING btree  ("group_id", "transaction_id" DESC);
