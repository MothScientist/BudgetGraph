SELECT
  "telegram_id"
FROM
  "budget_graph"."users_groups"
WHERE
  "group_id" = %(group_id)s::smallint