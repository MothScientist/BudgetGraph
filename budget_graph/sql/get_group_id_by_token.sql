SELECT
  "id"
FROM
  "budget_graph"."groups"
WHERE
  "token" = %(token)s::text