SELECT
  "timezone"
FROM
  "budget_graph"."users"
WHERE
  "telegram_id" = %(telegram_id)s::bigint