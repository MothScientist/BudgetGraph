UPDATE
    "budget_graph"."groups"
SET
    "owner" = %(telegram_id)s::bigint
WHERE
    "id" = %(group_id)s::smallint