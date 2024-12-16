UPDATE
  "budget_graph"."users"
SET
  "timezone" = %(timezone)s::smallint
WHERE
  "telegram_id" = %(telegram_id)s::bigint