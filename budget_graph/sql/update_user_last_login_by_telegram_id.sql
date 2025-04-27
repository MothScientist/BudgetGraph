UPDATE
  "budget_graph"."users"
SET
  "last_login" = current_timestamp AT TIME ZONE 'UTC'
WHERE
  "telegram_id" = %(telegram_id)s::bigint
RETURNING
  "last_login"