WITH
delete_record AS (
  DELETE FROM
    "budget_graph"."monetary_transactions"
  WHERE
    "group_id" = %(group_id)s::smallint AND
    "transaction_id" = %(transaction_id)s::integer
  RETURNING
    "transfer"
)
-- Correction of the 'total' field in all records following the one being deleted
UPDATE
  "budget_graph"."monetary_transactions"
SET
  "total" = "total" - (SELECT "transfer" FROM delete_record)
WHERE
  "group_id" = %(group_id)s::smallint AND
  "transaction_id" > %(transaction_id)s::integer