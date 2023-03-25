import sqlite3
import os
import datetime

WEEKDAYS = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]


class TogDatabase:
    def __init__(self, database: str):
        self.database = sqlite3.connect(database)
        self.database.row_factory = self.row_factory

    @staticmethod
    def row_factory(cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

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

    def find_trip(self, start_station: str, end_station: str, date: str, time: str):
        date1 = datetime.date.fromisoformat(date)
        date2 = date1 + datetime.timedelta(days=1)
        day1, day2 = WEEKDAYS[date1.weekday()], WEEKDAYS[date2.weekday()]

        day_1_trips = self.execute_sql_file("trip.sql", [day1, start_station, end_station])
        day_1_trips = [trip for trip in day_1_trips if trip['Tid'] >= time]

        day_2_trips = self.execute_sql_file("trip.sql", [day2, start_station, end_station])

        return day_1_trips, day_2_trips

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
