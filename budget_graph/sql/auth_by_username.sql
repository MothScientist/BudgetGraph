SELECT
    EXISTS (
        SELECT
            1
        FROM
            "budget_graph"."users"
        WHERE
            "username" = %(username)s::text
            AND
            "psw_hash" = %(psw_hash)s::text
)