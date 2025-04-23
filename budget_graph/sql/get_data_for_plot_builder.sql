WITH

usernames AS (
  SELECT
    users."username"
  FROM
    "budget_graph"."users_groups" users_groups
    JOIN "budget_graph"."users" users ON users."telegram_id" = users_groups."telegram_id"
  WHERE
    users_groups."group_id" = (SELECT "group_id" FROM "budget_graph"."users_groups" WHERE "telegram_id" = %(telegram_id)s::bigint)
    AND
    (
      %(diagram_type)s::smallint = 0 AND users."telegram_id" = %(telegram_id)s::bigint
      OR
      %(diagram_type)s::smallint = 1
    )
)

SELECT
  "username",
  SUM(CASE WHEN "transfer" > 0 THEN "transfer" ELSE 0 END) "incomeSum",
  SUM(CASE WHEN "transfer" < 0 THEN "transfer" ELSE 0 END) "expenseSum"
FROM
  "budget_graph"."monetary_transactions"
WHERE
  "username" = ANY(SELECT "username" FROM usernames)
  AND
  (
    (
      %(start_date)s::date IS NULL AND %(end_date)s::date IS NULL
    )
    OR
    (
      %(start_date)s::date IS NOT NULL AND %(end_date)s::date IS NOT NULL
      AND
      "record_date" BETWEEN %(start_date)s::date AND %(end_date)s::date
    )
    OR
    (
      %(start_date)s::date IS NOT NULL AND %(end_date)s::date IS NULL
      AND
      "record_date" >= %(start_date)s::date
    )
    OR
    (
      %(start_date)s::date IS NULL AND %(end_date)s::date IS NOT NULL
      AND
      "record_date" <= %(end_date)s::date
    )
  )
GROUP BY "username"