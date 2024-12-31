SELECT
    "language"
FROM
    "budget_graph"."user_languages_telegram"
WHERE
    "telegram_id" = %(telegram_id)s::bigint