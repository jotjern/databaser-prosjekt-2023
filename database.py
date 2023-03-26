import sqlite3
import os
import datetime

from utils import hms_to_seconds

WEEKDAYS = ["mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lørdag", "søndag"]


class TogDatabase:
    def __init__(self, database_file: str):
        self.database_file = database_file
        self.database = self.connect(database_file)

    def connect(self, database_file: str):
        database = sqlite3.connect(database_file)
        database.row_factory = self.row_factory
        return database

    @staticmethod
    def row_factory(cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    def is_initialized(self):
        return len(self.database.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite%';"
        ).fetchall()) > 0

    def list_routes_by_day_and_station(self, day: str, station: str):
        return self.execute_sql_file("routes_by_day_and_station.sql", [day, station])

    def add_customer(self, name: str, email: str, phone: str) -> int:
        return self.execute_sql_file("add_new_customer.sql", [name, email, phone])[0]["KundeNr"]

    def list_customers(self):
        return self.execute_sql_file("list_customers.sql", [])

    def route_weekdays(self, route_id: int):
        return [row["Ukedag"] for row in self.execute_sql_file("route_weekdays.sql", [route_id])]

    def add_route_instance(self, route_id: int, date: str):
        self.execute_sql_file("add_route_instance.sql", [route_id, date])

    def count_carriages_free_seats(self, route_id: int, date: str):
        return self.execute_sql_file("count_carriage_free_seats.sql", [route_id, date])

    def find_tickets(self, route_id: int, date: str):
        return self.execute_sql_file("find_tickets.sql", [route_id, date])

    def find_tickets_in_carriage(self, route_id: int, date: str, carriage_id: int):
        return self.execute_sql_file("find_tickets_in_carriage.sql", [route_id, date, carriage_id])

    def find_future_purchases_by_customer(self, customer_id: int):
        ret = []
        for purchase in self.execute_sql_file("find_purchases_by_customer.sql", [customer_id]):
            if datetime.datetime.strptime(purchase["Dato"], "%Y-%m-%d").date() >= datetime.datetime.now().date():
                ret.append(purchase)
        return ret

    def find_purchases_by_customer(self, customer_id: int):
        return self.execute_sql_file("find_purchases_by_customer.sql", [customer_id])

    def purchase_ticket(self, route_id: int, date: str, carriage_n: int, seat: int, customer: int, from_: str, to: str):
        order = self.create_order(customer)

        self.execute_sql_file(
            "purchase_ticket.sql",
            [route_id, date, seat, carriage_n, from_, to, order])

        return order

    def find_customer_by_name(self, name):
        return self.execute_sql_file("find_customer_by_name.sql", [name])[0]

    def create_order(self, customer_id: int):
        date = datetime.date.today().strftime("%Y-%m-%d")
        time = datetime.datetime.now().strftime("%H:%M")
        return self.execute_sql_file("create_order.sql", [date, time, customer_id])[0]["OrdreNr"]

    def list_routes(self):
        return self.execute_sql_file("list_routes.sql", [])

    def generate_route_instances(self, route_id: int, start_date: str, end_date: str):
        start_date = datetime.date.fromisoformat(start_date)
        end_date = datetime.date.fromisoformat(end_date)

        weekdays = self.route_weekdays(route_id)
        while start_date <= end_date:
            weekday = WEEKDAYS[start_date.weekday()]
            if weekday in weekdays:
                self.add_route_instance(route_id, start_date.strftime("%Y-%m-%d"))

            start_date += datetime.timedelta(days=1)

    def find_trips(self, start_station: str, end_station: str, date: str, time: str):
        date1 = datetime.date.fromisoformat(date)
        date2 = date1 + datetime.timedelta(days=1)
        day1, day2 = WEEKDAYS[date1.weekday()], WEEKDAYS[date2.weekday()]

        day_1_trips = self.execute_sql_file("trip.sql", [day1, start_station, end_station])
        day_1_trips = [trip for trip in day_1_trips if hms_to_seconds(trip['Avgang']) >= hms_to_seconds(time)]

        day_2_trips = self.execute_sql_file("trip.sql", [day2, start_station, end_station])

        return day_1_trips + day_2_trips

    def delete_database(self):
        if self.database_file != ":memory:" and os.path.exists(self.database_file):
            os.remove(self.database_file)
        self.database = self.connect(self.database_file)

    def reset_database(self):
        self.delete_database()
        self.execute_sql_script("init_togdb_tables.sql")
        self.execute_sql_script("init_togdb_data.sql")

        for route in self.list_routes():
            self.generate_route_instances(route["TogruteID"], "2023-04-03", "2023-04-04")

    def execute_sql_file(self, query_file: str, args: list, commit=True):
        with open(os.path.join("sql_queries", query_file), "r", encoding="utf-8") as fr:
            query = fr.read()

        cursor = self.database.execute(query, args)
        results = cursor.fetchall()
        if commit:
            self.database.commit()
        return results

    def execute_sql_script(self, script_file: str, commit=True):
        with open(os.path.join("sql_scripts", script_file), "r", encoding="utf-8") as fr:
            query = fr.read()

        self.database.executescript(query)
        if commit:
            self.database.commit()

    def execute_sql_script_ignore_errors(self, script_file: str, commit=True):
        with open(os.path.join("sql_scripts", script_file), "r", encoding="utf-8") as fr:
            query = fr.read()

        for query in query.split(";"):
            try:
                self.database.execute(query)
            except sqlite3.OperationalError:
                pass

        if commit:
            self.database.commit()
