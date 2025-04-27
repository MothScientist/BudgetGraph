SELECT
  EXISTS (
    SELECT
      1
    FROM
      "budget_graph"."groups"
    WHERE
      "token" = %(token)s::text
)
