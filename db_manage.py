import sqlite3
import os

from database import TogDatabase

if __name__ == "__main__":
    db = TogDatabase("database.db")
    print(db.list_routes_by_day_and_station("mandag", "Trondheim"))


