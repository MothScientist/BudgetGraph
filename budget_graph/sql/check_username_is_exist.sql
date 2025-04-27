SELECT
  EXISTS (
    SELECT
      1
    FROM
      "budget_graph"."users"
    WHERE
      LOWER("username") = LOWER(%(username)s::text) -- LOWER() -> username is case-insensitive
)