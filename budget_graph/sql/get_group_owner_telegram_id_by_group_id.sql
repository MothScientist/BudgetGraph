SELECT
    u."telegram_id"
FROM
    "budget_graph"."users" u
    JOIN "budget_graph"."groups" g ON u."telegram_id" = g."owner"
WHERE
    g."id" = %(group_id)s::smallint