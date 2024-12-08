UPDATE
    "budget_graph"."users"
SET
    "settings"[1] = NOT "settings"[1]
WHERE
    "telegram_id" = %(telegram_id)s::bigint