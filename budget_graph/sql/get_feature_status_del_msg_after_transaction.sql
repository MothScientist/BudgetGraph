SELECT
  "settings"[1]
FROM
  "budget_graph"."users"
WHERE
  "telegram_id" = %(telegram_id)s::bigint