DO $$ DECLARE
 r RECORD;
BEGIN
 FOR r IN (
           SELECT
             tablename
           FROM
             pg_tables
           WHERE
             schemaname = 'budget_graph'
           ) LOOP
   EXECUTE
   'DROP TABLE
   "budget_graph".'
   ||
   quote_ident(r.tablename)
   ||
   ' CASCADE';
 END LOOP;
END $$;

DO $$ DECLARE
 r RECORD;
BEGIN
 FOR r IN (
           SELECT
             routine_name
           FROM
             information_schema.routines
           WHERE
             specific_schema = 'budget_graph'
           ) LOOP
   EXECUTE
   'DROP FUNCTION
   "budget_graph".'
   ||
   quote_ident(r.routine_name)
   ||
   '() CASCADE';
 END LOOP;
END $$;

DO $$ DECLARE
 r RECORD;
BEGIN
 FOR r IN (
           SELECT
             trigger_name, event_object_table
           FROM
             information_schema.triggers
           WHERE
             trigger_schema = 'budget_graph'
           ) LOOP
   EXECUTE
     'DROP TRIGGER '
     ||
     quote_ident(r.trigger_name)
     ||
     ' ON "budget_graph".'
     ||
     quote_ident(r.event_object_table)
     ||
     ' CASCADE';
 END LOOP;
END $$;