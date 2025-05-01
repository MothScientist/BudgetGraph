SELECT
  "settings"[%(feature)s::smallint]
FROM
  "budget_graph"."users"
WHERE
  "telegram_id" = %(telegram_id)s::bigint