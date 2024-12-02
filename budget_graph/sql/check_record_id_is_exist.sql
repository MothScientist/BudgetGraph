SELECT
    EXISTS (
        SELECT
            1
        FROM
            "budget_graph"."monetary_transactions"
        WHERE
            "group_id" = %(group_id)s::smallint
            AND "transaction_id" = %(transaction_id)s::integer
    )