SELECT
    u."username",
    u."last_login"
FROM
    "budget_graph"."users" u
    JOIN "budget_graph"."users_groups" u_g ON u."telegram_id" = u_g."telegram_id"
WHERE
    u_g."group_id" = %s::smallint