-- Creating a new user (owner) and a new group
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
  ),

  user_group_id AS (
    INSERT INTO
      "budget_graph"."groups"
      ("owner", "token")
    VALUES
    (
      (SELECT "telegram_id" FROM "user_telegram_id"),
      %(token)s::text
    )
    RETURNING "id" AS "group_id"
  )

INSERT INTO
  "budget_graph"."users_groups"
  ("telegram_id", "group_id")
VALUES
(
  (SELECT "telegram_id" FROM "user_telegram_id"),
  (SELECT "group_id" FROM "user_group_id")
)