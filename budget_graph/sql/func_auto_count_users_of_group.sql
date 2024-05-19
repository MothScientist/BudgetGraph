-- Create a function with a trigger for automatically counting the number of participants in a group:
-- Functions to update the number of group members (INSERT)
CREATE OR REPLACE FUNCTION
  update_number_of_group_users()
RETURNS
  TRIGGER AS $update_number_of_group_users$
BEGIN
    UPDATE "budget_graph"."groups"
    SET "users_number" = (
        SELECT COUNT(*)
        FROM "budget_graph"."users"
        WHERE "group_id" = NEW."group_id"
    )
    WHERE "id" = NEW."group_id";
    RETURN NEW;
END;
  $update_number_of_group_users$
  LANGUAGE plpgsql;

-- Trigger for adding users
CREATE TRIGGER
    after_add_user
  AFTER
  INSERT
    ON "budget_graph"."users"
  FOR EACH ROW
  EXECUTE FUNCTION
    update_number_of_group_users();

-- Functions to update the number of group members (DELETE)
CREATE OR REPLACE FUNCTION
  update_number_of_group_users_after_delete()
RETURNS
  TRIGGER AS $update_number_of_group_users_after_delete$
BEGIN
    UPDATE "budget_graph"."groups"
    SET "users_number" = (
        SELECT COUNT(*)
        FROM "budget_graph"."users"
        WHERE "group_id" = OLD."group_id"
    )
    WHERE "id" = OLD."group_id";
    RETURN OLD;
END;
  $update_number_of_group_users_after_delete$
  LANGUAGE plpgsql;

-- Trigger for deleting users
CREATE TRIGGER
    after_delete_user
  AFTER
  DELETE
  ON "budget_graph"."users"
  FOR EACH ROW
  EXECUTE FUNCTION
    update_number_of_group_users_after_delete();