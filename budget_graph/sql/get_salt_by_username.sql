SELECT
    "psw_salt"
FROM
    "budget_graph"."users"
WHERE
    "username" = %(username)s::text