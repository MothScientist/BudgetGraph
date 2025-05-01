UPDATE
    "budget_graph"."users"
SET
    "settings"[%(feature)s::smallint] = NOT "settings"[%(feature)s::smallint]
WHERE
    "telegram_id" = %(telegram_id)s::bigint