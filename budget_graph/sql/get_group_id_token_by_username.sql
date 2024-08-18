SELECT
 g."token", g."id"
FROM
 "budget_graph"."groups" g
INNER JOIN "budget_graph"."users_groups" u_g ON g."id" = u_g."group_id"
INNER JOIN "budget_graph"."users" u USING("telegram_id")
WHERE
 u."username" = %(username)s::text