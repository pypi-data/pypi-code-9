
# This function, when attached to a table as a trigger, will publish all
# changes to that table using Postgres's NOTIFY feature.  Changes will be
# published to a channel with the same name as the table.

# The payload for each change will be the complete row, serialized to JSON,
# with an additional 'tg_op' key that specifies the operation done to the table
# (INSERT, UPDATE, or DELETE).

# In the case of delete operations, the old row will be returned instead of the
# new.

# Note that this implies that no row, after being serialized to JSON, may
# exceed 8000 bytes (the limit on NOTIFY).  If you try, the write will fail.
# If you need rows that big, and want notifications on changes to them, you
# should change this function to publish just the primary key column(s), and
# then the listening application can query for the entire row.
NOTIFY_FUNC = """
CREATE OR REPLACE FUNCTION tables_notify_func() RETURNS trigger as $$
DECLARE
  payload text;
BEGIN
    IF TG_OP = 'DELETE' THEN
    payload := row_to_json(tmp)::text FROM (
            SELECT
                OLD.*,
                TG_OP
        ) tmp;
    ELSE
        payload := row_to_json(tmp)::text FROM (
            SELECT
                NEW.*,
                TG_OP
        ) tmp;
    END IF;

  PERFORM pg_notify(TG_TABLE_NAME::text, payload);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""


NOTIFY_TRIG = """
CREATE TRIGGER {tablename}_notify_trig
AFTER INSERT OR UPDATE OR DELETE
ON {tablename}
FOR EACH ROW EXECUTE PROCEDURE tables_notify_func();
"""

def create_tables_notify_func(conn):
    cur = conn.cursor()
    cur.execute(NOTIFY_FUNC)
    conn.commit()
    return cur

def create_table_notify_trigger(conn, tablename):
    cur = conn.cursor()
    cur.execute(NOTIFY_TRIG.format(tablename=tablename))
    conn.commit()
    return cur
