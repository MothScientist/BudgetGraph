-- Adding a new user to an existing group
WITH
  user_telegram_id AS (
    INSERT INTO
      "budget_graph"."users"
      ("telegram_id", "username", "psw_salt", "psw_hash", "last_login")
    VALUES
      (
        %(telegram_id)s::bigint,
        %(username)s::text,
        %(psw_salt)s::text,
        %(psw_hash)s::text,
        current_timestamp AT TIME ZONE 'UTC'
      )
    RETURNING
      "telegram_id"
  )
INSERT INTO
  "budget_graph"."users_groups"
  ("telegram_id", "group_id")
VALUES
(
  (SELECT "telegram_id" FROM "user_telegram_id"),
  %(group_id)s::smallint
)