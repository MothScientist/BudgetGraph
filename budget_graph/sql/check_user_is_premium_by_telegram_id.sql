SELECT
  "premium_status"
FROM
  "budget_graph"."premium_users"
WHERE
  "telegram_id" = %(telegram_id)s::bigint