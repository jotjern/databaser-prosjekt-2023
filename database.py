import sqlite3
import os


class TogDatabase:
    def __init__(self, database: str):
        self.database = sqlite3.connect(database)

    def is_initialized(self):
        return len(self.database.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name = 'Jernbanestasjon';"
        ).fetchall()) == 1

    def list_routes_by_day_and_station(self, day: str, station: str):
        return self.execute_sql_file("routes_by_day_and_station.sql", [day, station])

    def add_customer(self, name: str, email: str, phone: str):
        return self.execute_sql_file("add_new_customer.sql", [name, email, phone])

    def list_customers(self):
        return self.execute_sql_file("list_customers.sql", [])

    def delete_database(self):
        self.execute_sql_script("delete_togdb_tables.sql")

    def reset_database(self):
        if self.is_initialized():
            self.delete_database()

        self.execute_sql_script("init_togdb_tables.sql")
        self.execute_sql_script("init_togdb_data.sql")

    def execute_sql_file(self, query_file: str, args: list, commit=True):
        with open(os.path.join("sql_queries", query_file), "r", encoding="utf-8") as fr:
            query = fr.read()

        results = self.database.execute(query, args).fetchall()
        if commit:
            self.database.commit()
        return results

    def execute_sql_script(self, script_file: str, commit=True):
        with open(os.path.join("sql_scripts", script_file), "r", encoding="utf-8") as fr:
            query = fr.read()

        self.database.executescript(query)
        if commit:
            self.database.commit()
