-- Create a function with a trigger that will itself generate a transaction number within one group:
CREATE OR REPLACE FUNCTION
  set_transaction_id()
RETURNS
  TRIGGER AS $set_transaction_id$
BEGIN
    -- Determine the number of the last entry in the group
    SELECT COALESCE(MAX("transaction_id"), 0) + 1  -- COALESCE is required if the table is still empty
    INTO NEW."transaction_id"
    FROM "budget_graph"."monetary_transactions"
    WHERE "group_id" = NEW."group_id";

    RETURN NEW;
END;
  $set_transaction_id$
  LANGUAGE plpgsql;

CREATE TRIGGER
    "before_insert_new_transaction"
  BEFORE
  INSERT
    ON "budget_graph"."monetary_transactions"
  FOR EACH ROW
  EXECUTE FUNCTION
    set_transaction_id();