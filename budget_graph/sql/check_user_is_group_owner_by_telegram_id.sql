SELECT
  "owner" = %(owner)s::bigint
FROM
  "budget_graph"."groups"
WHERE
  "id" = %(group_id)s::smallint