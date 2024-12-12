SELECT
    "telegram_id"
FROM
    "budget_graph"."users"
WHERE
    "username" = %(username)s::text