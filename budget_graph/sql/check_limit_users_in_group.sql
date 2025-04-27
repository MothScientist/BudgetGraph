SELECT
 "users_number" IS NOT NULL AND "users_number" <> 20
FROM
 "budget_graph"."groups"
WHERE
 "id" = %(group_id)s::smallint