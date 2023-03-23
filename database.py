from typing import Literal, Any, List
import sqlite3
import os

Weekday = Literal["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]


class TogDatabase:
    def __init__(self, database: str):
        self.database = sqlite3.connect(database)

    def list_routes_by_day_and_station(self, day: Weekday, station: str):
        return self.execute_sql_file("routes_by_day_and_station.sql", [day, station])

    def add_customer(self, name: str, email: str, phone: str):
        return self.execute_sql_file("add_new_customer.sql", [name, email, phone])

    def execute_sql_file(self, query_file: str, args: List[Any]):
        with open(os.path.join("queries", query_file), "r", encoding="utf-8") as fr:
            query = fr.read()

        print(args)

        return self.database.execute(query, args).fetchall()

