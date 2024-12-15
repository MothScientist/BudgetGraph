SELECT
    u."username"
FROM
    "budget_graph"."users" u
    JOIN "budget_graph"."groups" g ON u."telegram_id" = g."owner"
WHERE
    g."id" = %s::smallint