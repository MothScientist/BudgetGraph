-- Creating Indexes
-- to get a list of group users:
CREATE        INDEX IF NOT EXISTS "users_group_id"                       ON "budget_graph"."users_groups"          USING btree ("group_id");

-- to check the uniqueness of the username:
CREATE UNIQUE INDEX IF NOT EXISTS "users_lower_username"                 ON "budget_graph"."users"                 USING btree (LOWER("username"));

-- to get a list of group transactions:
CREATE        INDEX IF NOT EXISTS "transactions_group_id"                ON "budget_graph"."monetary_transactions" USING btree ("group_id", "record_date" ASC);

-- to search for a specific record:
CREATE UNIQUE INDEX IF NOT EXISTS "transactions_transaction_id_group_id" ON "budget_graph"."monetary_transactions" USING btree ("transaction_id" DESC, "group_id");

-- to get the latest entries by date
CREATE        INDEX IF NOT EXISTS "transactions_last_records_index"      ON "budget_graph"."monetary_transactions" USING btree ("group_id", "record_date" DESC);

-- Indexes for analytics
-- to collect statistics for a certain period:
CREATE        INDEX IF NOT EXISTS "transactions_group_id_record_date"    ON "budget_graph"."monetary_transactions" USING btree ("group_id", "record_date" DESC);
CREATE        INDEX IF NOT EXISTS "transactions_username_record_date"    ON "budget_graph"."monetary_transactions" USING btree ("group_id", "username", "record_date" DESC);