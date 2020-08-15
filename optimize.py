import psycopg2
from psycopg2._psycopg import cursor, connection

from config import dbauth

conn: connection = psycopg2.connect(**dbauth)
conn.autocommit = True
cur: cursor = conn.cursor()
for table in ["episode", "line", "person", "phrase", "series"]:
    cur.execute("VACUUM (ANALYZE, FULL, VERBOSE) " + table)
    for notice in conn.notices:
        print(notice)
    conn.notices = []

for table in ["episode", "line", "person", "phrase", "series"]:
    cur.execute("REINDEX (VERBOSE) table " + table)
    for notice in conn.notices:
        print(notice)
    conn.notices = []

