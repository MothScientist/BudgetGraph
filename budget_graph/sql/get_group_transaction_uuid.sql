SELECT
    COALESCE("transactions_uuid"::text, '')
FROM
    "budget_graph"."groups"
WHERE
    "id" = %(group_id)s::smallint