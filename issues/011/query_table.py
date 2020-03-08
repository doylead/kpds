import psycopg2
from psycopg2 import sql
from os import environ

yt_api_key = environ['YT_API_KEY']
connstring = "dbname='kpds'"
conn = psycopg2.connect(connstring)
cur = conn.cursor()

## Creates table with caps-sensitive schema and table name
# WIP
query = sql.SQL("create table {schema_table} (a INT, b INT)").format(
        schema_table = sql.Identifier("YouTube_Video_Stats","Test")
        )
cur.execute(query)
conn.commit()

## Checks to see if a table with caps-sensitive schema and
## table name exists
# WIP

## Adds a value to a table with a caps-sensitive schema
## and table name
# Works for one column
query = sql.SQL("insert into {schema_table} ({fields}) values (%s,%s)").format(
        schema_table = sql.Identifier("YouTube_Video_Stats","Test"),
        fields = sql.SQL(",").join([
            sql.Identifier("a"),
            sql.Identifier("b")
            ])
        )

values = [1,2]
cur.execute(query,values)

## Query table with caps-sensitive schema and table name
# Works as intended
query = sql.SQL("select {fields} from {schema_table}").format(
        fields = sql.SQL(",").join([
            sql.Identifier("a"),
            sql.Identifier("b")
            ]),
        schema_table = sql.Identifier("YouTube_Video_Stats","Test")
        )

cur.execute(query)
result = cur.fetchall()
print(result)

