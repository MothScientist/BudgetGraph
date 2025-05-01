SELECT
  "settings"[2:4]
FROM
  "budget_graph"."users"
WHERE
  "telegram_id" = %(telegram_id)s::bigint