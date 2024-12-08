SELECT
    CASE
        WHEN "owner" = %(owner)s::bigint THEN TRUE
        ELSE FALSE
    END
FROM
    "budget_graph"."groups"
WHERE
    "id" = %(group_id)s::smallint