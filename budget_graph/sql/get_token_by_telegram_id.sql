SELECT
    g."token"
FROM
    "budget_graph"."groups" g
    JOIN "budget_graph"."users_groups" u_g ON g."id" = u_g."group_id"
WHERE
    u_g."telegram_id" = %(telegram_id)s::bigint