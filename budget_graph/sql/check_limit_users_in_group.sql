SELECT
 CASE
    WHEN
      "users_number" IS NOT NULL
      AND
      "users_number" <> 20
    THEN
      TRUE
    ELSE
      FALSE
 END
FROM
 "budget_graph"."groups"
WHERE
 "id" = %(group_id)s::smallint