CREATE OR REPLACE FUNCTION update_transaction_uuid()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE "budget_graph"."groups"
    SET transactions_uuid = gen_random_uuid()
    WHERE id = NEW.group_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_transaction_uuid
AFTER INSERT OR UPDATE ON "budget_graph"."monetary_transactions"
FOR EACH ROW
EXECUTE FUNCTION update_transaction_uuid();
