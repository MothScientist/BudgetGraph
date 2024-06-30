WITH
user_info AS (
  SELECT u."username", u."telegram_id", u_g."group_id"
  FROM "budget_graph"."users" u
  INNER JOIN "budget_graph"."users_groups" u_g
  ON u."telegram_id" = u_g."telegram_id"
  WHERE
    (%(telegram_id)s::bigint IS NOT NULL AND u."telegram_id" = %(telegram_id)s::bigint) OR
    (%(username)s::text IS NOT NULL AND u."username" = %(username)s::text)
  LIMIT 1 -- to avoid collisions
),
new_record AS (
  INSERT INTO
    "budget_graph"."monetary_transactions"
    ("group_id", "username", "total", "transfer", "record_date", "category", "description")
  VALUES
    (
      (SELECT "group_id" FROM user_info),
      (SELECT "username" FROM user_info),
      %(transaction_amount)s::integer + -- transaction_amount + total
        (SELECT -- Gets the last 'total' amount in table by group ID. Returns 0 if there are no records.
          COALESCE(
            (
              SELECT
                "total"
              FROM
                "budget_graph"."monetary_transactions"
              WHERE
                "group_id" = (SELECT "group_id" FROM user_info) AND
                "record_date" <=  %(record_date)s::date
              ORDER BY
                "record_date" DESC,
                "transaction_id" DESC
              LIMIT 1
            ), 0)
        ),
      %(transaction_amount)s::integer,
      %(record_date)s::date,
      %(category)s::text,
      %(description)s::text
    )
  RETURNING "transaction_id", "transfer", "record_date"
)
UPDATE
  "budget_graph"."monetary_transactions"
SET
  "total" = "total" + (SELECT "transfer" FROM new_record)
WHERE
  "group_id" = (SELECT "group_id" FROM user_info) AND
  -- for the current date we do not have a record with a higher ID value than the new one
  "record_date" > (SELECT "record_date" FROM new_record)