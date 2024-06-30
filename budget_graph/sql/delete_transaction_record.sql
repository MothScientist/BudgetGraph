WITH
delete_record AS (
  DELETE FROM
    "budget_graph"."monetary_transactions"
  WHERE
    "group_id" = %(group_id)s::smallint AND
    "transaction_id" = %(transaction_id)s::integer
  RETURNING
    "transfer", "record_date", "transaction_id", "group_id"
)
-- Correction of the 'total' field in all records following the one being deleted
UPDATE
  "budget_graph"."monetary_transactions"
SET
  "total" = "total" - (SELECT "transfer" FROM delete_record)
WHERE
  "group_id" = (SELECT "group_id" FROM delete_record) AND
  -- within one date, the order of transactions is determined using the identifier: the higher, the newer the record
  (
    (
      "record_date" = (SELECT "record_date" FROM delete_record) AND
      "transaction_id" > (SELECT "transaction_id" FROM delete_record)
    )
    OR
    "record_date" > (SELECT "record_date" FROM delete_record)
  )