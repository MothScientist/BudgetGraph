SELECT
    "group_id"
FROM
    "budget_graph"."users_groups"
WHERE
    "telegram_id" = %(telegram_id)s::bigint