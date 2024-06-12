from os import makedirs, path
from sys import path as sys_path
sys_path.append('../')
from budget_graph.db_manager import connect_db, close_db  # noqa


def drop_tables_in_db() -> None:
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
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
                        """)
            conn.commit()
    except Exception as err:
        print(f'Critical error when deleting tables in the database: {err}')
    finally:
        close_db(conn)


def create_directories() -> None:
    try:
        makedirs('csv_tables', exist_ok=True)
        makedirs('logs', exist_ok=True)
    except Exception as err:
        print(f'Error creating additional directories: {err}')


def create_tables_in_db() -> None:
    """
    Creating a Database Infrastructure
    """
    conn = connect_db()
    sql_filenames: tuple = ('create_db', 'indexes', 'func_transaction_number', 'func_auto_count_users_of_group')
    try:
        with conn.cursor() as cur:
            for filename in sql_filenames:
                with open(path.join(path.dirname(__file__), f'sql/{filename}.sql'), 'r') as sql_file:
                    cur.execute(sql_file.read())
            conn.commit()
    except Exception as err:
        print(f'Critical error when creating tables in the database: {err}')
    finally:
        close_db(conn)


if __name__ == '__main__':
    drop_tables_in_db()
    create_directories()
    create_tables_in_db()
