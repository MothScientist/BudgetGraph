UPDATE
    "budget_graph"."groups"
SET
    "owner" = %s::bigint
WHERE
    "id" = %(group_id)s::smallint