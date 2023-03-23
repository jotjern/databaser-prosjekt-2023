import sqlite3
import os

if os.path.exists("database.db"):
    os.remove("database.db")

db = sqlite3.connect("database.db")

with open("togdb_tables.sql", "r", encoding="utf-8") as fr:
    init_query = fr.read()

with open("togdb_data.sql", "r", encoding="utf-8") as fr:
    data_query = fr.read()

db.execute("BEGIN TRANSACTION;")
for query in (init_query + data_query).split(";"):
    try:
        db.execute(query)
    except sqlite3.Error:
        print(query)
        raise
db.execute("COMMIT;")

db.commit()

print("Database initialized")


